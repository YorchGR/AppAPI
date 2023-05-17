from models.UserDb import UserDb, completeUserData, getUserByIdForm, getUserDbbyUserName, checkMail, checkNick
from classes.Constants import InternalConstants as const
from schemas.UserApp import UserAppBasic,UserAppComplete
from fastapi.security import OAuth2PasswordRequestForm
from models.PasswDb import PasswDb, getPasswDbByIdUser
from fastapi import APIRouter, status, Depends, Form
from classes.Security import AccessToken, JwtToken, refreshToken
from classes.Tools import Tools
from classes.Constants import ExternalMessages as ext
from datetime import datetime, timedelta
from dbConector import DbConector
from typing import Annotated
from sqlalchemy import func
from decouple import config


#Variables y métodos
router = APIRouter(prefix = "/users", tags = ["Users"], responses = {status.HTTP_404_NOT_FOUND:{"mesage": "Not found"}})
db = DbConector.getInstance()
session = db.getSession()

#Endpoints de Users
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
    completeUserData(newUser)
    return newUser

#Aún siendo post, estamos leyendo, así que se clasifica como Read
@router.post("/login")
async def login(formData: OAuth2PasswordRequestForm = Depends()):
    user = getUserDbbyUserName(formData.username)
    passwd = getPasswDbByIdUser(user.id_cont)
    passwd.checkPassword(formData.password, passwd.contrasena)
    accessToken = AccessToken(user.nick_us, datetime.now() + timedelta(minutes = int(config(const.ACCESS_TOKEN_EXPIRE_MINUTES))))
    jwToken = JwtToken(accessToken)
    return jwToken

#Read user previamente logueado
@router.get("/me",  response_model = UserAppComplete)
async def getMyUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    return completeUserData(user)


#El guión bajo se usa para asignar el resultado a una variable que no se va a usar 
@router.get("/{id}",  response_model = UserAppBasic)
async def getUserById(id: str, _: Annotated[UserDb, Depends(JwtToken.authUserToken)]):
    return completeUserData(getUserByIdForm(id))

#Actualización de usuario
@router.put("/me/update")
async def updateUser(user: Annotated[UserDb, Depends(JwtToken.authUserToken)], nombreForm: str = Form(...), apellidoForm: str = Form(...), nickForm: str = Form(...), passwForm: str = Form(...), emailForm: str = Form(...)):
    if user is not None:
        nombreForm = user.updateUserNombre(nombreForm)
        apellidoForm = user.updateUserApellido (apellidoForm)
        nickForm = user.updateUserNick(nickForm)
        emailForm = user.updateUserMail(emailForm) 
        updatedUser = UserDb(user.id_usuario, nombreForm, apellidoForm, nickForm, emailForm, user.id_cont)
        currentPassword = getPasswDbByIdUser(user.id_cont)
        updatedPassword = PasswDb(user.id_cont, user.id_usuario, currentPassword) 
        updatedPassword.updateUserContrasena(passwForm)
        userComplete = UserAppComplete.createUserCompletDict(updatedUser.id_usuario, updatedUser.nombre_us, updatedUser.apellido_us, updatedUser.nick_us, updatedUser.email_us, updatedPassword.contrasena, updatedPassword.id_cont)
        jwToken = refreshToken(updatedUser)
        updateUserAndPasswordInDataBase(updatedUser, updatedPassword)
    else:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.GENERIC_ERROR)     
    return getResponseDataUserUpdate(userComplete, jwToken)


def getResponseDataUserUpdate(userComplete: UserAppComplete, jwToken:JwtToken) -> dict:
    responseData = {
        "user_data": userComplete,
        "jwt_token": jwToken,
    }
    return responseData

def updateUserAndPasswordInDataBase(updatedUser: UserDb, updatedPassword: PasswDb) -> None:
    session.merge(updatedUser)
    session.merge(updatedPassword)
    session.commit()
   
def addNewUserInDataBase(newUser: UserDb, newUserPassw: PasswDb):
    session.add(newUser)
    session.add(newUserPassw)
    session.commit()




#@router.get("/", response_model = List[UserAppComplete])
#async def get_all_users():
#    return session.query(UserDb).all()

