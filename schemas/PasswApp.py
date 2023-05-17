from pydantic import BaseModel, Field



class PasswApp(BaseModel):
    id_cont: int = Field(..., example = "5")
    id_usuario: int = Field(..., example = "1")
    contrasena: str = Field(..., min_length = 3, max_length = 255, example = "secreto25")
    
    def __init__(self, id_cont: int, id_usuario: int, contrasena: str):
        self.id_cont = id_cont
        self.id_usuario = id_usuario
        self.contrasena = contrasena  
       
