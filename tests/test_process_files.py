import pytest
import os
from iap.repository.db import (
    get_engine,
    get_session_factory,
    get_tm_session,
    Base
    )
import transaction
from pyramid import testing
from iap.repository.db.warehouse import Entity
from iap.data_processing.data_proc_manager import Loader
from iap.repository.db.warehouse import Warehouse


from sqlalchemy.orm import sessionmaker

xfail = pytest.mark.xfail


# def dummy_request(dbsession):
#     return testing.DummyRequest(dbsession=dbsession)


class TestProcessFiles:

    def setup_class(self):
        # self.config = testing.setUp(settings={
        #     'sqlalchemy.url': 'sqlite:///:memory:'
        # })
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///IAP.sqlite'
        })
        self.config.include('iap.repository.db')
        settings = self.config.get_settings()
        self.engine = get_engine(settings)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(autoflush=False)
        session_factory.configure(bind=self.engine)

        # session_factory = get_session_factory(self.engine)

        root = Entity(name='root', layer='root', dimension='root')
        curr_ssn = session_factory()
        curr_ssn.add(root)
        curr_ssn.commit()

        self.wh = Warehouse(session_factory)

        # self.db_session = get_tm_session(session_factory,
        # transaction.manager)

        # self.db_session.add(root)
        # transaction.manager.commit()


    def test_dimensions(self):
        loader = Loader(self.wh, data_load_command='jj')
        loader.load()
        # transaction.manager.commit()
        # assert 5 == 5
        print('ss')
