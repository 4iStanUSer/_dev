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

@pytest.fixture
def token(web_app):
    """
    Feature preparetion login and authentification

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    token = str(res.json_body['data'])
    return token


def test_get_tools_info(web_app):
    """
    Test for view get_tools_with_projects

    :param web_app:
    :type web_app: webtest.app.TestApp
    :return:
    :rtype: None
    """
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    token = str(res.json_body['data'])

    res = web_app.post_json('/get_tools_with_projects', {'X-Token': token})

    expected = {"data": {"projects": [{"id": 1, "name": "Oral Care Forecasting", "description": null}, {"id": 2, "name": "Lean Forecasting", "description": null}], "tools": [{"id": 1, "name": "Forecasting", "description": "This is forecasting"}]}, "error": False}
    actual = res.json
    assert actual['data']['projects']==expected['data']['projects']
