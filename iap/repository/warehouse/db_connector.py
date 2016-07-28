from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from IAP import CONFIG


Base = declarative_base()

class DBConnector():
    '''
    Class to connect database.
    '''
    def __init__(self):
        '''
        Configure and run engine for work with database via scoped session.
        '''
        self.__base = Base
        self.__engine = create_engine(CONFIG.get_db_connection_string())
        self.__session_factory = scoped_session(sessionmaker(bind=self.__engine, 
                                           autoflush=False))
        self.__db_session = self.__session_factory()
        self.__base.metadata.create_all(bind=self.__engine)

    def close_session(self):
        '''
        Close database session.
        '''
        self.__db_session.close()

    @property
    def session(self):
        '''
        Returns active session.
        '''
        return self.__db_session


