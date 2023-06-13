from sqlalchemy import Column, String, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from dbConector import DbConector
from datetime import datetime


Base = declarative_base()
db = DbConector.getInstance()
session = db.getSession()

class ControlDb(Base):
    __tablename__ = 'CONTROL'
    id_control = Column("id_control", String(255), primary_key = True)
    id_pregunta = Column("id_pregunta", String(255))
    id_usuario = Column("id_usuario", Integer())
    id_respuesta_us = Column("id_respuesta_us", String(255))
    fecha_control = Column("fecha_control", DateTime(), nullable = False)

    def __init__(self, id_control: str, id_pregunta: str, id_usuario: int, id_respuesta_us: str, fecha_control: datetime):
        self.id_control = id_control
        self.id_pregunta = id_pregunta
        self.id_usuario = id_usuario
        self.id_respuesta_us = id_respuesta_us
        self.fecha_control = fecha_control
