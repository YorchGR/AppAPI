from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class SectionDb(Base):
    __tablename__ = 'SECCION'
    id_seccion = Column("id_seccion", String(255), primary_key = True)
    nombre_seccion = Column("nombre_seccion", String(255))
    id_ley = Column("id_ley", String(255))
    id_titulo = Column("id_titulo", String(255))
    id_capitulo = Column("id_capitulo", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default=datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default=datetime.now())

    def __init__(self, id_seccion: str, nombre_seccion: str, id_ley: str, id_titulo: str, id_capitulo: str, estado: str):
        self.id_seccion = id_seccion
        self.nombre_seccion = nombre_seccion
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.id_capitulo = id_capitulo
        self.estado = estado
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
