from pydantic import BaseModel, Field
from datetime import datetime

class AskApp(BaseModel):
    id_pregunta: str = Field(..., max_length = 255, example = "PRG-1")
    enunciado_pr: str = Field(..., max_length = 255, example = "Enunciado de pregunta")
    id_estructura: str = Field(..., max_length = 255, example = "EST-1")
    id_ley: str = Field(..., max_length = 255, example = "LEY-1")
    id_titulo: str = Field(..., max_length = 255, example = "TIT-1")
    id_capitulo: str = Field(..., max_length = 255, example = "CAP-1")
    id_seccion: str = Field(..., max_length = 255, example = "SEC-1")
    id_subseccion: str = Field(..., max_length = 255, example = "SUB-1")
    id_articulo: str = Field(..., max_length = 255, example = "Artículo de ejemplo")
    estado: str = Field(..., max_length=1, example = "1")
    fecha_alta: datetime = Field(..., example = datetime.now())
    fecha_mod: datetime = Field(..., example = datetime.now())

    def __init__(self, id_pregunta: str, enunciado_pr: str, id_estructura: str, id_ley: str, id_titulo: str, id_capitulo: str, id_seccion: str, id_subseccion: str, id_articulo: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_pregunta = id_pregunta
        self.enunciado_pr = enunciado_pr
        self.id_estructura = id_estructura
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.id_capitulo = id_capitulo
        self.id_seccion = id_seccion
        self.id_subseccion = id_subseccion
        self.id_articulo = id_articulo
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod