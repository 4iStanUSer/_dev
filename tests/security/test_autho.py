from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('../')
print(os.curdir)

@pytest.fixture
def web_app():
    settings = get_appsettings(os.path.join(ABS_PATH, 'test.ini'), name='main')
    app = main(global_config = None, **settings)
    from webtest import TestApp
    testapp = TestApp(app)
    return testapp


def test_model_overview(web_app):
    feature = ["Forecast Dashboard","Saved Scenario", "Compare", "Simulator / Scenario Editor"]
    res = web_app.post('/model_overview', {'feature':feature})
