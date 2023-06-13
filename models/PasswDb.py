from sqlalchemy.ext.declarative import declarative_base
from classes.Constants import ExternalMessages as ext
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext 
from dbConector import DbConector
from classes.Tools import Tools
from passlib.hash import bcrypt
from datetime  import datetime
from fastapi import  status



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
crypt = CryptContext(schemes = ["bcrypt"])
Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class PasswDb(Base):
    __tablename__ = 'CONTRASENA'
    id_cont = Column("id_cont", Integer(), nullable = False, unique = True)
    __mapper_args__ = {"primary_key":id_cont}
    id_usuario = Column("id_usuario", Integer(), unique = True)
    contrasena = Column("contrasena", String(255), nullable = False)
    fecha_act = Column("fecha_act", String(255), nullable = False, default = datetime.now())
    
    def __init__(self, id_cont: int, id_usuario: int, contrasena: str):
        self.id_cont = id_cont
        self.id_usuario = id_usuario
        self.contrasena = contrasena
        self.fecha_act = datetime.now()
               
    def updateUserContrasena(self, passwForm: str) -> None:
        if passwForm != None and passwForm != '': 
            self.contrasena = PasswDb.encryptPassword(passwForm)
    
    def checkPassword(self, formPasswd: str, userPasswd:str) -> None:
        if not crypt.verify(formPasswd, userPasswd):
            raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_PASSWORD) 
    
    def encryptPassword(password: str) -> str:
        return bcrypt.hash(password)
        
def getPasswDbByIdUser(id: str) -> PasswDb:
    userPass = session.query(PasswDb).filter(PasswDb.id_usuario == id).first()
    if not userPass:
        raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_PASSWORD) 
    return userPass