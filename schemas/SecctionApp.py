from pydantic import BaseModel, Field
from datetime import datetime

class SectionApp(BaseModel):
    id_seccion: str = Field(..., max_length = 255, example = "SEC-1")
    nombre_seccion: str = Field(..., max_length = 255, example = "Nombre de la sección")
    id_ley: str = Field(..., max_length = 255, example = "LEY-1")
    id_titulo: str = Field(..., max_length = 255, example = "TIT-1")
    id_capitulo: str = Field(..., max_length = 255, example = "CAP-1")
    estado: str = Field(..., max_length = 1, example = "1")
    fecha_alta: datetime = Field(..., example = datetime.now())
    fecha_mod: datetime = Field(..., example = datetime.now())

    def __init__(self, id_seccion: str, nombre_seccion: str, id_ley: str, id_titulo: str, id_capitulo: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_seccion = id_seccion
        self.nombre_seccion = nombre_seccion
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.id_capitulo = id_capitulo
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod
