from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class StructureDb(Base):
    __tablename__ = 'ESTRUCTURA'
    id_estructura = Column("id_estructura", String(255), primary_key = True)
    id_ley = Column("id_ley", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default = datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default = datetime.now())

    def __init__(self, id_estructura: str, id_ley: str, estado: str):
        self.id_estructura = id_estructura
        self.id_ley = id_ley
        self.estado = estado
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
