from enum import Enum

class InternalConstants(str, Enum):
    BBDD_USERNAME = 'BBDD_USERNAME'
    BBDD_PASSWORD = 'BBDD_PASSWORD'
    BBDD_HOST = 'BBDD_HOST'
    BBDD_PORT = 'BBDD_PORT'
    BBDD_SERVICE = 'BBDD_SERVICE'
    JWT_SK = 'JWT_SK'
    ALGORITHM = 'ALGORITHM'
    ACCESS_TOKEN_EXPIRE_MINUTES = 'ACCESS_TOKEN_EXPIRE_MINUTES'
    ORACLE_CONECTION = 'ORACLE_CONECTION'
    SERVICE = 'SERVICE'
    
class ExternalMessages(str, Enum):
    GENERIC_ERROR = "Se ha producido un error."
    INVALID_MAIL_ERROR = "Se ha producido un error actualizando el email del usuario."
    INVALID_CREDENTIALS = "Credenciales no válidas."
    INVALID_PASSWORD = "La contraseña no es correcta."
    REGISTRED_USER = "Usuario registrado."
    REGISTRED_NICK_USER = "Este nick se encuentra registrado."
    REGISTRED_MAIL = "Este email se encuentra registrado."
    INVALID_USER_NAME = "El nombre de usuario no es correcto."
    INVALID_USER_ROL = "No tienes el rol necesario para realizar esta acción."
    DISABLED_USER = "El usuario se encuentra deshabilitado."
    DELETE_SOFT_USER = "El usuario se ha deshabilitado."
    DELETE_HARD_USER = "El administrador ha eliminado a un usuario."
    DELETE_ERROR = "No puedes eliminar a un usuario activo o con rol de administrador"
    
    