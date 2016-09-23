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
from iap.data_processing.data_loading.common import tl_weekly_to_month_445,\
    week_to_month
import datetime

xfail = pytest.mark.xfail



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

    @pytest.mark.skip
    def test_loader(self):
        loader = Loader(self.wh, data_load_command='jj')
        loader.load()
        # transaction.manager.commit()
        # assert 5 == 5
        print('ss')

    @pytest.mark.skip(reason="no need to test now")
    def test_weekly_converter(self):
        label = week_to_month(2016, 13)
        print(label)
        start_date = datetime.datetime(year=2015, month=1, day=1)
        first_label, time_line = tl_weekly_to_month_445(start_date, 53, 1)
        print(first_label)
        for key in time_line:
            print(time_line[key])
