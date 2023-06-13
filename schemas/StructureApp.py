from pydantic import BaseModel, Field
from datetime import datetime

class StructureApp(BaseModel):
    id_estructura: str = Field(..., max_length = 255, example = "EST-1")
    id_ley: str = Field(..., max_length = 255, example = "LEY-1")
    estado: str = Field(..., max_length = 1, example="1")
    fecha_alta: datetime = Field(..., example = datetime.now())
    fecha_mod: datetime = Field(..., example = datetime.now())

    def __init__(self, id_estructura: str, id_ley: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_estructura = id_estructura
        self.id_ley = id_ley
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod
