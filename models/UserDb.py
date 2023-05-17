from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from classes.Tools import Tools
from fastapi import status
from datetime  import datetime
from dbConector import DbConector
from models.PasswDb import getPasswDbByIdUser
from classes.Constants import ExternalMessages as ext

Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class UserDb(Base):
    __tablename__ = 'USUARIOS'
    id_usuario = Column("id_usuario", Integer(), nullable = False, primary_key = True)
    __mapper_args__ = {"primary_key": id_usuario}
    nombre_us = Column("nombre_us", String(50), nullable = False)
    apellido_us = Column("apellido_us", String(50), nullable = False)
    nick_us = Column("nick_us", String(30), nullable = False, unique = True)
    email_us = Column("email_us", String(30), nullable = False, unique = True)
    id_cont = Column("id_cont", Integer(), unique = True)
    rol_us = Column("rol_us", Integer(), unique = True)
    estado_us = Column("estado_us", Integer(), nullable = False, default = 1)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default = datetime.now())
    fecha_act = Column("fecha_act", DateTime(), nullable = False, default = datetime.now())
    
    def __init__(self, id_usuario: int, nombre_us: str, apellido_us: str, nick_us: str, email_us: str, id_cont: int, rol_us: int = 0, estado_us: str = 1):
        self.id_usuario = id_usuario
        self.nombre_us = nombre_us
        self.apellido_us = apellido_us
        self.nick_us = nick_us
        self.email_us = email_us
        self.id_cont = id_cont
        self.rol_us = rol_us
        self.estado_us = estado_us
        self.fecha_alta = datetime.now()
        self.fecha_act = datetime.now()

    def updateUserNombre(self, nombreForm: str) ->str:
        if nombreForm != None or nombreForm != '':
            if nombreForm != self.nombre_us:
                self.nombre_us = nombreForm
        return self.nombre_us
    
    def updateUserApellido(self, apellidoForm: str) ->str:
        if apellidoForm != None or apellidoForm != '':
            if apellidoForm != self.apellido_us:
                self.apellido_us = apellidoForm
        return self.apellido_us
    
    def updateUserNick(self, nickForm: str) ->str:
        if nickForm != None or nickForm != '':
            if nickForm != self.nick_us:
                checkNick(nickForm)
                self.nick_us = nickForm
        return self.nick_us    
    
    def updateUserMail(self, emailForm: str) -> str:
        if emailForm != None or emailForm != '':
            if emailForm != self.email_us:
                checkNick(emailForm)
                self.email_us = emailForm
        return self.email_us  
    
    def updateUserState(self, estado_us: str) -> None:
            self.estado_us = estado_us
        
    def completeUserData(self) -> None:
        if not self:
            raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_CREDENTIALS)
        passwd = getPasswDbByIdUser(self.id_cont)
        self.contrasena = passwd.contrasena

def checkUserActive(user: UserDb) -> None:
    if user.estado_us == 0:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.DISABLED_USER)
 
def checkUserAdmin(user: UserDb) -> None:
    if user.rol_us != 1:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_USER_ROL)    

def getUserByIdForm(id: str) -> UserDb:
    user = session.query(UserDb).get(id)
    if not user:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.REGISTRED_USER)
    return user

def getUserDbbyUserName(userName: str) -> UserDb:
    user = session.query(UserDb).filter(UserDb.nick_us == userName).first()
    if not user:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_USER_NAME)
    checkUserActive(user)
    return user

def checkMail(emailForm: str) -> None:
    sameEmail = session.query(UserDb).filter(UserDb.email_us == emailForm).first()
    if sameEmail:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.REGISTRED_MAIL) 
    
def checkNick(nickForm: str) -> None:
    sameEmail = session.query(UserDb).filter(UserDb.nick_us == nickForm).first()
    if sameEmail:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.REGISTRED_NICK_USER) 