from classes.Constants import InternalConstants as const
from classes.Constants import ExternalMessages as ext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dbConector import DbConector
from models.UserDb import UserDb
from decouple import config
from jose import jwt,JWTError
from typing import Annotated


oauth2 = OAuth2PasswordBearer(tokenUrl = "login")
db = DbConector.getInstance()
session = db.getSession()

class AccessToken:
   def __init__(self, nick: any, exp: any):
      self.ATDict = {}
      self.ATDict["nick"] = nick
      self.ATDict["exp"] = exp

class JwtToken:
    def __init__(self, access_token: AccessToken):
        self.jwtDict= {}
        self.jwtDict["access_token"] = JwtToken.createAccessToken(access_token)
        self.jwtDict["token_type"] = "bearer"

    def createAccessToken(access_token: AccessToken) -> str:
        accessToken = jwt.encode(access_token.ATDict, config(const.JWT_SK), algorithm = config(const.ALGORITHM))
        return accessToken
    
    def authUserToken(jwToken: Annotated[str, Depends(oauth2)]) -> UserDb:
        exception = HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail =  ext.INVALID_CREDENTIALS,
                headers = {"WWW-Authenticate": "Bearer"})
        try:
            userName = jwt.decode(jwToken, config(const.JWT_SK), algorithms = [config(const.ALGORITHM)]).get("nick")
            if userName is None:
                raise exception
            user = session.query(UserDb).filter(UserDb.nick_us == userName).first()
            return user
        except JWTError:
            raise exception
        
def refreshToken(user: UserDb) -> JwtToken:
    accessToken = AccessToken(user.nick_us, datetime.now() + timedelta(minutes = int(config(const.ACCESS_TOKEN_EXPIRE_MINUTES))))
    jwToken = JwtToken(accessToken)
    return jwToken