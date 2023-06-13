from models.UserDb import UserDb, getUserByIdForm, getUserDbbyUserName, checkMail, checkNick
from classes.Constants import InternalConstants as const
from fastapi.security import OAuth2PasswordRequestForm
from models.PasswDb import PasswDb, getPasswDbByIdUser
from classes.Constants import ExternalMessages as ext
from fastapi import APIRouter, status, Depends, Form
from classes.Security import AccessToken, JwtToken
from schemas.UserApp import UserAppComplete
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
    newUser.completeUserData()
    return newUser

#Read user: Aún siendo post, estamos leyendo, así que se clasifica como read
@router.post("/login")
async def login(formData: OAuth2PasswordRequestForm = Depends()):
    user = getUserDbbyUserName(formData.username)
    passwd = getPasswDbByIdUser(user.id_cont)
    passwd.checkPassword(formData.password, passwd.contrasena)
    accessToken = AccessToken(user.id_usuario, datetime.now() + timedelta(minutes = int(config(const.ACCESS_TOKEN_EXPIRE_MINUTES))))
    jwToken = JwtToken(accessToken)
    return jwToken

#Read user: Muestra los datos de un usuario previamente logueado. Se pude cambiar el response_model por otro más simple
@router.get("/me", response_model = UserAppComplete)
async def getMyUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    if user is not None:
        user.checkUserActive()
        user.completeUserData()
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.GENERIC_ERROR)
    return user

#Update user: Actualización de user
@router.put("/me/update", response_model = UserAppComplete)
async def updateUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)], nombreForm: str = Form(...), apellidoForm: str = Form(...), nickForm: str = Form(...), passwForm: str = Form(...), emailForm: str = Form(...)):
    if user is not None:
        user.checkUserActive()
        user.updateUserNombre(nombreForm)
        user.updateUserApellido (apellidoForm)    
        user.updateUserNick(nickForm)
        user.updateUserMail(emailForm) 
        user.updateFechaAct()
        currentPassword = getPasswDbByIdUser(user.id_cont)
        currentPassword.updateUserContrasena(passwForm)
        updateUserAndPasswordInDataBase(user, currentPassword)
        user.contrasena = currentPassword.contrasena
        return user
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.GENERIC_ERROR)  
    
#Update user: cambia el estado del usuario a 1
@router.put("/admin/reactive/{id}", response_model = UserAppComplete)
async def reactivetUserWithIdByAdmin(id: str, user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    userToReactive = getUserByIdForm(id)  
    user.checkUserAdmin()
    if userToReactive.estado_us == 0:
        userToReactive.updateUserState(1)
        userToReactive.updateFechaAct()
        userPasswordToReactive = getPasswDbByIdUser(userToReactive.id_cont)
        userToReactive.contrasena = userPasswordToReactive.contrasena
        session.merge(userToReactive)
        session.commit()
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_REACTIVE_USER)   
    return userToReactive
    
#Delete soft user: cambia el estado del usuario a 0, lo que se considera un borrado soft
@router.put("/deleteme")
async def deleteSoftUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    user.checkUserActive()
    if user.rol_us == 1:
         raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_DISABLE_ADMIN)   
    user.updateUserState(0)
    user.updateFechaAct()
    session.merge(user)
    session.commit()
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_SOFT_USER)

#Delete soft user: Un usuario con rol de admin, cambia el estado del usuario a 0, lo que se considera un borrado soft
@router.put("/admin/deleteme/soft/{id}")
async def deleteSoftUser(id: str, user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    user.checkUserActive()
    user.checkUserAdmin()
    userToDelete = getUserByIdForm(id)
    userToDelete.updateUserState(0)
    userToDelete.updateFechaAct()
    session.merge(userToDelete)
    session.commit()
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_SOFT_USER)

#Delete hard user: autentico borrado, solo si se tiene el rol de administrador
@router.delete("/admin/delete/hard/{id}")
async def deleteHardUserByAdmin(id: str, user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    user.checkUserActive()
    user.checkUserAdmin()
    userToDelete = getUserByIdForm(id)
    userPasswordToDelete = getPasswDbByIdUser(id)
    deleteUserByUserAdmin(userToDelete, userPasswordToDelete)
    return Tools.getRaise(status.HTTP_200_OK, ext.DELETE_HARD_USER)


#Métodos de user_services:------------------------------------------------------------------------------------------------------
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
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.DELETE_ERROR) 

