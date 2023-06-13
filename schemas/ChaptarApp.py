from pydantic import BaseModel, Field
from datetime import datetime

class ChapterApp(BaseModel):
    id_capitulo: str = Field(..., max_length = 255, example="CAP-1")
    nombre_capitulo: str = Field(..., max_length = 255, example="Nombre del capítulo")
    id_ley: str = Field(..., max_length = 255, example="LEY-1")
    id_titulo: str = Field(..., max_length = 255, example="TIT-1")
    estado: str = Field(..., max_length = 1, example="1")
    fecha_alta: datetime = Field(..., example=datetime.now())
    fecha_mod: datetime = Field(..., example=datetime.now())

    def __init__(self, id_capitulo: str, nombre_capitulo: str, id_ley: str, id_titulo: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_capitulo = id_capitulo
        self.nombre_capitulo = nombre_capitulo
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod
