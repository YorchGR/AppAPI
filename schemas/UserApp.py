from classes.Constants import ExternalMessages as ext
from pydantic import BaseModel, EmailStr, Field
from email_validator import validate_email, EmailNotValidError
from classes.Tools import Tools
from datetime import datetime
from fastapi import status


class UserAppComplete(BaseModel):
    id_usuario: int | None = Field(example = 5)
    nombre_us: str | None = Field(min_length = 3, max_length = 50, example = "Jorge")
    apellido_us: str | None = Field(min_length = 3, max_length = 50, example = "López")
    nick_us: str | None = Field(min_length = 3, max_length = 30, example = "Yorch83")
    email_us: EmailStr | None = Field(example = "myemail@gmail.com")
    contrasena: str | None = Field(min_length = 3, max_length = 255, example = "secreto25")
    id_cont: int | None
    estado_us: str | None = Field(min_length = 1, max_length = 1, example = "1", default = "1")
    rol_us: str | None = Field(min_length = 1, max_length = 1, example = "1", default = "0")
    fecha_alta : datetime = Field(datetime.now())
    fecha_act: datetime = Field(datetime.now())
    
    class Config:
        orm_mode = True
        
    def createUserCompletDict(id_usuario: int, nombre_us: str, apellido_us: str, nick_us: str, email_us: str, contrasena: str, id_cont: int, estado_us: str = "1", rol_us: str = "0") -> dict:
        UserAppComplete.validateUserMailComposition(email_us)
        newUserCompleteDict = {
            "id_usuario": id_usuario,
            "nombre_us": nombre_us,
            "apellido_us": apellido_us,
            "nick_us": nick_us,
            "email_us": email_us,
            "contrasena": contrasena,
            "id_cont": id_cont,
            "estado_us": estado_us,
            "rol_us": rol_us,
            "fecha_alta": datetime.now(),
            "fecha_act": datetime.now()
        }
        return newUserCompleteDict
        
    def validateUserMailComposition(email_us: str) -> None:
        try:
            validate_email(email_us)
        except EmailNotValidError:
            raise Tools.getRaise(status.HTTP_400_BAD_REQUEST, ext.INVALID_MAIL_ERROR)



class UserAppBasic(BaseModel):
    nombre_us: str | None = Field(min_length = 3, max_length = 50, example = "Jorge")
    nick_us: str | None = Field(min_length = 3, max_length = 30, example = "Yorch83")
    email_us: EmailStr | None = Field(example = "myemail@gmail.com")
    contrasena: str | None = Field(min_length = 3, max_length = 255, example = "secreto25")
    
    class Config:
            orm_mode = True
            
    def createUserBasicDict(nombre_us: str, nick_us: str, email_us: str, contrasena: str) -> dict:
        user_dict = {
            "nombre_us": nombre_us,
            "nick_us": nick_us,
            "email_us": email_us,
            "contrasena": contrasena
        }
        return user_dict

