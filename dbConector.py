from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config
from classes.Constants import InternalConstants as const


class DbConector:
    __instance = None
    
    @staticmethod
    def getInstance():
        """ Static access method. """
        if DbConector.__instance == None:
            DbConector()
        return DbConector.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if DbConector.__instance != None:
            raise Exception("Conexión creada")
        else:
            engine = create_engine(f"{config(const.ORACLE_CONECTION)}://{config(const.BBDD_USERNAME)}:{config(const.BBDD_PASSWORD)}@{config(const.BBDD_HOST)}:{config(const.BBDD_PORT)}/{config(const.SERVICE)}={config(const.BBDD_SERVICE)}")
            Session = sessionmaker(engine)
            self.session = Session()
            DbConector.__instance = self
    
    def getSession(self):
        return self.session

    