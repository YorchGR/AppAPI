from pydantic import BaseModel, Field
from datetime import datetime

class AnswerssApp(BaseModel):
    id_respuesta: str = Field(..., max_length = 255, example = "RSP-1")
    id_pregunta: str = Field(..., max_length = 255, example = "PRG-1")
    enunciado_res: str = Field(..., max_length = 255, example = "Esta es la respuesta.")
    valoracion: str = Field(..., max_length = 1, example = "0")
    explicacion: str = Field(..., max_length = 255, example = "Aquí está la explicación.")
    estado: str = Field(..., max_length = 1, example = "1")
    fecha_alta: datetime = Field(..., default = datetime.now)
    fecha_mod: datetime = Field(..., default = datetime.now)

    def __init__(self, id_respuesta: str, id_pregunta: str, enunciado_res: str, valoracion: str, explicacion: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_respuesta = id_respuesta
        self.id_pregunta = id_pregunta
        self.enunciado_res = enunciado_res
        self.valoracion = valoracion
        self.explicacion = explicacion
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod