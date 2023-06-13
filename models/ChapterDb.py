from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class ChapterDb(Base):
    __tablename__ = 'CAPITULO'
    id_capitulo = Column("id_capitulo", String(255), primary_key = True)
    nombre_capitulo = Column("nombre_capitulo", String(255))
    id_ley = Column("id_ley", String(255))
    id_titulo = Column("id_titulo", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False)
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False)

    def __init__(self, id_capitulo: str, nombre_capitulo: str, id_ley: str, id_titulo: str, estado: str, fecha_alta: datetime, fecha_mod: datetime):
        self.id_capitulo = id_capitulo
        self.nombre_capitulo = nombre_capitulo
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.estado = estado
        self.fecha_alta = fecha_alta
        self.fecha_mod = fecha_mod
