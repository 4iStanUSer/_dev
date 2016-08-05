import pytest
import os
from iap.repository.warehouse.meta import Base
from iap.repository.warehouse import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
import transaction
import sys
import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy
from pyramid import testing
from iap.repository.warehouse.wh_common import *

xfail = pytest.mark.xfail


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class TestDbInterface:

    def setup_class(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        # self.config = testing.setUp(settings={
        #     'sqlalchemy.url': 'sqlite:///IAP.sqlite'
        # })
        self.config.include('iap.repository.warehouse')
        settings = self.config.get_settings()
        self.engine = get_engine(settings)
        Base.metadata.create_all(self.engine)
        session_factory = get_session_factory(self.engine)
        # self.session = get_tm_session(session_factory, transaction.manager)
        self.db_session = get_tm_session(session_factory, transaction.manager)

        self.test = 'test'

    def test_add_variables(self):
        variables_properties = {
            'Sales Value':
                {'data_type': 'float',
                 'var_type': 'general',
                 'metric': 'US Dollars',
                 'units_multiplier': 1000}}

    @xfail(run=False)
    def test_dimensions(self):
        dimensions = {'Product': ['Category', 'Segment', 'Brand']}
        set_dimensions(self.db_session, dimensions)
        new_client = add_client(ssn=self.db_session, name='Project1',
                                code='Prj1')
        new_user = add_user(ssn=self.db_session, email='test@test.com',
                            password='pass', client=new_client)
        self.db_session.flush()
        print('Dimensions test = ' + self.test)
        assert 5 == 5
