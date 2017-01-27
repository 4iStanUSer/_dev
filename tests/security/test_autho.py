from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('../')
print(os.curdir)
import json
from access_rights import rights

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
    res = web_app.post_json('/login', {'data':{"username": login, 'password': password}})
    token = str(res.json_body['data'])
    return token

def setup_module():
    server = web_app()
    res = server.post_json("/test_preparation", {'test_name': "authorisation"})
    print(res)


def test_authorisation_success_expected(web_app, token):

    res = web_app.post_json('/forecast/get_scenarios_list', {'X-Token': token})
    expected = {"error": False}
    actual = res.json
    print(actual)

    assert actual["error"] == expected["error"]

def test_authorisation_error_expected(web_app, token):

    res = web_app.post_json('/forecast/mark_as_final', {'X-Token': token})
    expected = {"error": True}
    actual = res.json
    print(actual)

    assert actual["error"] == expected["error"]