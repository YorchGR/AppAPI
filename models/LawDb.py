from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class LawDb(Base):
    __tablename__ = 'LEY'
    id_ley = Column("id_ley", String(255), primary_key = True)
    nombre_ley = Column("nombre_ley", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default = datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default = datetime.now())

    def __init__(self, id_ley: str, nombre_ley: str, estado: str):
        self.id_ley = id_ley
        self.nombre_ley = nombre_ley
        self.estado = estado
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
