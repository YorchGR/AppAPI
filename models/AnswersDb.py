from sqlalchemy import Column, String, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class AnswerDb(Base):
    __tablename__ = 'RESPUESTA'
    id_respuesta = Column("id_respuesta", String(255), primary_key = True)
    id_pregunta = Column("id_pregunta", String(255))
    enunciado_res = Column("enunciado_res", String(255))
    valoracion = Column("valoracion", String(1), nullable = False)
    explicacion = Column("explicacion", String(255))
    estado = Column("estado", String(1), nullable = False)
    fecha_alta = Column("fecha_alta", DateTime(), nullable = False, default=datetime.now())
    fecha_mod = Column("fecha_mod", DateTime(), nullable = False, default=datetime.now())

    def __init__(self, id_respuesta: str, id_pregunta: str, enunciado_res: str, valoracion: str, explicacion: str, estado: str):
        self.id_respuesta = id_respuesta
        self.id_pregunta = id_pregunta
        self.enunciado_res = enunciado_res
        self.valoracion = valoracion
        self.explicacion = explicacion
        self.estado = estado
        self.fecha_alta = datetime.now()
        self.fecha_mod = datetime.now()
