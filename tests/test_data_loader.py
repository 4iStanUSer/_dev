from pyramid.paster import get_appsettings
import pytest
import os
from iap import main

ABS_PATH = os.path.abspath('../')


@pytest.fixture
def web_app():
    """
    Fixture for server preparation

    :return:
    :rtype: webtest.app.TestApp
    """
    settings = get_appsettings(os.path.join(ABS_PATH, 'test.ini'), name='main')
    app = main(global_config=None, **settings)
    from webtest import TestApp
    testapp = TestApp(app)
    return testapp


def test_data_loader_without_regime():
    from iap.data_loading.data_loader import Loader
    loader = Loader()
    loader.run_processing("JJOralCare_config")


def test_data_loader_indy_regime():
    from iap.data_loading.data_loader import Loader
    settings = "C:/Users\Alex/Desktop/dev/iap/data_storage/data_lake"
    loader = Loader(settings)
    loader.run_processing("Avon_MMM")


def test_data_loader_warehouse_regime():
    from iap.data_loading.data_loader import Loader
    db_config = "sqlite:///C:/Users/Alex/Desktop/dev/iap/IAP.sqlite"
    settings = "C:/Users\Alex/Desktop/dev/iap/data_storage/data_lake"
    loader = Loader(settings, db_config)
    loader.run_processing("JJOralCare_config")





