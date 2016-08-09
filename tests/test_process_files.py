import pytest
import os
from iap.repository.warehouse import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
import transaction
from pyramid import testing
from iap.repository.warehouse.wh_common import *
from iap.data_processing.data_proc_manager import Loader

xfail = pytest.mark.xfail


# def dummy_request(dbsession):
#     return testing.DummyRequest(dbsession=dbsession)


class TestProcessFiles:

    def setup_class(self):
        pass
        # self.config = testing.setUp(settings={
        #     'sqlalchemy.url': 'sqlite:///:memory:'
        # })
        # # self.config = testing.setUp(settings={
        # #     'sqlalchemy.url': 'sqlite:///IAP.sqlite'
        # # })
        # self.config.include('iap.repository.warehouse')
        # settings = self.config.get_settings()
        # self.engine = get_engine(settings)
        # Base.metadata.create_all(self.engine)
        # session_factory = get_session_factory(self.engine)
        # self.db_session = get_tm_session(session_factory, transaction.manager)
        #
        # self.test = 'test'


    @xfail(run=True)
    def test_dimensions(self):
        loader = Loader('jj')
        loader.load()
        assert 5 == 5
