from models.UserDb import UserDb, getUserByIdForm, getUserDbbyUserName, checkMail, checkNick, checkUserActive, checkUserAdmin
from classes.Security import AccessToken, JwtToken, refreshToken
from classes.Constants import InternalConstants as const
from schemas.UserApp import UserAppBasic,UserAppComplete
from fastapi.security import OAuth2PasswordRequestForm
from models.PasswDb import PasswDb, getPasswDbByIdUser
from classes.Constants import ExternalMessages as ext
from fastapi import APIRouter, status, Depends, Form
from datetime import datetime, timedelta
from dbConector import DbConector
from classes.Tools import Tools
from typing import Annotated
from sqlalchemy import func
from decouple import config


#Variables de user_services:----------------------------------------------------------------------------------------------
router = APIRouter(prefix = "/users", tags = ["Users"], responses = {status.HTTP_404_NOT_FOUND:{"mesage": "Not found"}})
db = DbConector.getInstance()
session = db.getSession()

#Endpoints de Users:------------------------------------------------------------------------------------------------------
#Create user
@router.post("/signup", response_model = UserAppComplete)
async def setNewUser(nombreForm: str = Form(...), apellidoForm: str = Form(...), nickForm: str = Form(...), passwForm: str = Form(...), emailForm: str = Form(...)):
    checkMail(emailForm)
    checkNick(nickForm)
    lastIdUsuario = (session.query(func.max(UserDb.id_usuario)).scalar()) + 1
    lastIdCont = (session.query(func.max(PasswDb.id_cont)).scalar()) + 1
    passwForm = PasswDb.encryptPassword(passwForm)
    newUser = UserDb(lastIdUsuario , nombreForm, apellidoForm, nickForm, emailForm, lastIdCont)
    newUserPassw = PasswDb(lastIdCont, lastIdUsuario, passwForm)
    addNewUserInDataBase(newUser, newUserPassw)
    newUser = UserDb(lastIdUsuario , nombreForm, apellidoForm, nickForm, emailForm, lastIdCont)
    newUser.completeUserData()
    return newUser

#Read user: Aún siendo post, estamos leyendo, así que se clasifica como read
@router.post("/login")
async def login(formData: OAuth2PasswordRequestForm = Depends()):
    user = getUserDbbyUserName(formData.username)
    passwd = getPasswDbByIdUser(user.id_cont)
    passwd.checkPassword(formData.password, passwd.contrasena)
    accessToken = AccessToken(user.nick_us, datetime.now() + timedelta(minutes = int(config(const.ACCESS_TOKEN_EXPIRE_MINUTES))))
    jwToken = JwtToken(accessToken)
    return jwToken

#Read user: Muestra los datos de un usuario previamente logueado. Se pude cambiar el response_model por otro más simple
@router.get("/me", response_model = UserAppComplete)
async def getMyUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    if user is not None:
        user.completeUserData()
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.GENERIC_ERROR)
    return user

#Update user: Actualización de user
@router.put("/me/update")
async def updateUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)], nombreForm: str = Form(...), apellidoForm: str = Form(...), nickForm: str = Form(...), passwForm: str = Form(...), emailForm: str = Form(...)):
    if user is not None:
        checkUserActive(user)
        nombreForm = user.updateUserNombre(nombreForm)
        apellidoForm = user.updateUserApellido (apellidoForm)
        refreshActualToken = checkIfRefreshToken(user, nickForm)        
        nickForm = user.updateUserNick(nickForm)
        emailForm = user.updateUserMail(emailForm) 
        updatedUser = UserDb(user.id_usuario, nombreForm, apellidoForm, nickForm, emailForm, user.id_cont)
        currentPassword = getPasswDbByIdUser(user.id_cont)
        updatedPassword = PasswDb(user.id_cont, user.id_usuario, currentPassword) 
        updatedPassword.updateUserContrasena(passwForm)
        userComplete = UserAppComplete.createUserCompletDict(updatedUser.id_usuario, updatedUser.nombre_us, updatedUser.apellido_us, updatedUser.nick_us, updatedUser.email_us, updatedPassword.contrasena, updatedPassword.id_cont)
        updateUserAndPasswordInDataBase(updatedUser, updatedPassword)
        jwToken = updateToken(refreshActualToken, updatedUser)
        responseData = getResponseDataUserUpdate(userComplete, jwToken)
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.GENERIC_ERROR)  
    if refreshActualToken:   
        return responseData
    else:
        return userComplete
    
#Update user: cambia el estado del usuario a 1
@router.put("/admin/reactive/{id}")
async def reactivetUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    checkUserActive(user)
    checkUserAdmin(user)
    userToReactive = getUserByIdForm(id)
    userToReactive.updateUserState(1)
    session.merge(user)
    session.commit()
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_SOFT_USER)

#Delete soft user: cambia el estado del usuario a 0, lo que se considera un borrado soft
@router.put("/deleteme")
async def deleteSoftUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    checkUserActive(user)
    user.updateUserState(0)
    session.merge(user)
    session.commit()
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_SOFT_USER)

#Delete hard user: autentico borrado, solo si se tiene el rol de administrador
@router.delete("/admin/delete/{id}")
async def deleteHardUserByAdmin(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    checkUserActive(user)
    checkUserAdmin(user)
    userToDelete = getUserByIdForm(id)
    userPasswordToDelete = getPasswDbByIdUser(id)
    deleteUserByUserAdmin(userToDelete, userPasswordToDelete)
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_HARD_USER)


#Métodos de user_services:------------------------------------------------------------------------------------------------------
def getResponseDataUserUpdate(userComplete: UserAppComplete, jwToken:JwtToken) -> dict:
    responseData = {
        "user_data": userComplete,
        "jwt_token": jwToken,
    }
    return responseData

def checkIfRefreshToken(user: UserDb, nickForm: str) -> bool:
    if nickForm != None or nickForm != '':
        return nickForm != user.nick_us
    else:
        return False
  
def updateToken(refreshActualToken: bool, updatedUser: UserDb):
    if refreshActualToken:
       return refreshToken(updatedUser)  

def updateUserAndPasswordInDataBase(updatedUser: UserDb, updatedPassword: PasswDb) -> None:
    session.merge(updatedUser)
    session.merge(updatedPassword)
    session.commit()
   
def addNewUserInDataBase(newUser: UserDb, newUserPassw: PasswDb):
    session.add(newUser)
    session.add(newUserPassw)
    session.commit()

def deleteUserByUserAdmin(userToDelete: UserDb, userPasswordToDelete: PasswDb):
    if userToDelete.rol_us != 1 and userToDelete.estado_us == 0:
        session.delete(userToDelete)
        session.delete(userPasswordToDelete)
        session.commit()
    else:
        return Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.DELETE_ERROR) 


# #El guión bajo se usa para asignar el resultado a una variable que no se va a usar 
# @router.get("/{id}",  response_model = UserAppBasic)
# async def getUserById(id: str, _: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
#     return completeUserData(getUserByIdForm(id))

#@router.get("/", response_model = List[UserAppComplete])
#async def get_all_users():
#    return session.query(UserDb).all()

