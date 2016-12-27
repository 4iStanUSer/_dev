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


def test_scenario(web_app):
    res = web_app.get("/forecast/get_scenarios_list")
    print(res)


def test_create_scenario(web_app):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    scenario_data = {"name": "Scenario",
                     "description": "some description",
                     "status": "new",
                     "shared": "True",
                     "geographie": "Ukraine",
                     "product": "Salo",
                     "channel": "Main"}

    res = web_app.post_json("/forecast/create_scenario", scenario_data)
    print(res)

def test_get_scenario_description(web_app):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/get_scenario_description", {'id': 0})
    print(res)