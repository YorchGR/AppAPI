from pydantic import BaseModel, Field
from datetime import datetime

class LawApp(BaseModel):
    id_ley: str = Field(..., max_length = 255, example = "LEY-1")
    nombre_ley: str = Field(..., max_length = 255, example = "Nombre de la ley")
    estado: str = Field(..., max_length =  1, example = "1")
    fecha_alta: datetime = Field(..., example = datetime.now())
    fecha_mod: datetime = Field(..., example = datetime.now())

    def __init__(self, id_ley: str, nombre_ley: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_ley = id_ley
        self.nombre_ley = nombre_ley
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod
