from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime

Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class SubsecctionDb(Base):
    __tablename__ = 'SUBSECCION'
    id_subseccion = Column("id_subseccion", String(255), primary_key = True)
    nombre_subseccion = Column("nombre_subseccion", String(255))
    id_ley = Column("id_ley", String(255))
    id_titulo = Column("id_titulo", String(255))
    id_capitulo = Column("id_capitulo", String(255))
    id_seccion = Column("id_sección", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default=datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default=datetime.now())

    def __init__(self, id_subseccion: str, nombre_subseccion: str, id_ley: str, id_titulo: str, id_capitulo: str, id_seccion: str, estado: str):
        self.id_subseccion = id_subseccion
        self.nombre_subseccion = nombre_subseccion
        self.id_ley = id_ley
        self.id_titulo = id_titulo
        self.id_capitulo = id_capitulo
        self.id_seccion = id_seccion
        self.estado = estado
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
