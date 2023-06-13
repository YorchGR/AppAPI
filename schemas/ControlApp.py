from pydantic import BaseModel, Field
from datetime import datetime

class ControlApp(BaseModel):
    id_control: str = Field(..., max_length = 255, example = "CONT-1")
    id_pregunta: str = Field(..., max_length = 255, example = "PRG-1")
    id_usuario: str = Field(..., max_length = 255, example = "1")
    id_respuesta_us: str = Field(..., max_length = 255, example = "RSP-1")
    fecha_control: datetime = Field(..., example = datetime.now())

    def __init__(self, id_control: str, id_pregunta: str, id_usuario: str, id_respuesta_us: str, fecha_control: datetime):
        self.id_control = id_control
        self.id_pregunta = id_pregunta
        self.id_usuario = id_usuario
        self.id_respuesta_us = id_respuesta_us
        self.fecha_control = fecha_control
