from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class ArticleDb(Base):
    __tablename__ = 'ARTICULO'
    id_articulo = Column("id_articulo", String(255), primary_key = True)
    nombre_articulo = Column("nombre_articulo", String(255))
    id_ley = Column("id_ley", String(255))
    id_titulo = Column("id_titulo", String(255))
    id_capitulo = Column("id_capitulo", String(255))
    id_seccion = Column("id_seccion", String(255))
    id_subseccion = Column("id_subseccion", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False)
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False)

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
