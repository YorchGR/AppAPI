from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class AskDb(Base):
    __tablename__ = 'PREGUNTA'
    id_pregunta = Column("id_pregunta", String(255), primary_key = True)
    enunciado_pr = Column("enunciado_pr", String(255))
    id_estructura = Column("id_estructura", String(255))
    id_ley = Column("id_ley", String(255))
    id_titulo = Column("id_titulo", String(255))
    id_capitulo = Column("id_capitulo", String(255))
    id_seccion = Column("id_seccion", String(255))
    id_subseccion = Column("id_subseccion", String(255))
    id_articulo = Column("id_articulo", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default=datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default=datetime.now())

    def __init__(self, id_pregunta: str, enunciado_pr: str, id_estructura: str, id_ley: str, id_titulo: str, id_capitulo: str, id_seccion: str, id_subseccion: str, id_articulo: str, estado: str):
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
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
