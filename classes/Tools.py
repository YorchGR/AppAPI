from fastapi import HTTPException

class Tools:
    def getRaise(status_code: int, message: str):
        return HTTPException(status_code = status_code, detail = message, headers = {"WWW-Authenticate": "Bearer"})