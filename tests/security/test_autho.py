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


def test_model_overview(web_app):
    #res = web_app.post_json('/model_overview', {'data': rights})
    #print(res)
    pass

def test_authorisation(web_app):
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    print(res)
    token = str(res.json_body['data'])

    res = web_app.post_json('/check_auth', {'X-Token': token})
    expected = {"data": token, "error": False}
    actual = res.json
    print(actual)

    res = web_app.post_json('/', {'X-Token': token})
    expected = {"data": token, "error": False}
    actual = res.json
    print(actual)

    assert actual == expected