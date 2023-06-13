from pydantic import BaseModel, Field
from datetime import datetime


class ArticleApp(BaseModel):
    id_articulo: str = Field(..., max_length = 255, example = "ART-76")
    nombre_articulo: str = Field(..., max_length = 255, example = "Nombre de Artículo de ejemplo")
    id_ley: str = Field(..., max_length = 255, example = "LEY-1")
    id_titulo: str = Field(..., max_length = 255, example = "TIT-1")
    id_capitulo: str = Field(..., max_length = 255, example = "CAP-1")
    id_seccion: str = Field(..., max_length = 255, example = "SEC-1")
    id_subseccion: str = Field(..., max_length = 255, example = "SUB-1")
    estado: str = Field(..., max_length = 1, example = "1")
    fecha_alta: datetime = Field(...)
    fecha_mod: datetime = Field(...)

    def __init__(self, id_articulo: str, nombre_articulo: str, id_ley: str, id_titulo: str, id_capitulo: str, id_seccion: str, id_subseccion: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_articulo = id_articulo
        self.nombre_articulo = nombre_articulo
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.id_capitulo = id_capitulo
        self.id_seccion = id_seccion
        self.id_subseccion = id_subseccion
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod