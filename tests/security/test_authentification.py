from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('../')
print(os.curdir)


@pytest.fixture
def jwt():
    jwt = {'iss': '', "password": '', "exp_date": " ", "alg": "HS256"}
    return jwt


@pytest.fixture
def web_app():
    settings = get_appsettings(os.path.join(ABS_PATH, 'test.ini'), name='main')
    app = main(global_config = None, **settings)
    from webtest import TestApp
    testapp = TestApp(app)
    return testapp


def test_login(web_app):
    res = web_app.post_json('/login')
    token = str(res.json_body['token'])
    print(token)
    next_res = web_app.post('/check_auth', headers={'X-Token': token})
    print(next_res)


def test_loggedin(web_app):
    res = web_app.post_json('/check_auth')
    print(res)


def test_main_page(web_app):
    res = web_app.post_json('/login')
    token = str(res.json_body['token'])
    print(token)
    next_res = web_app.post('/check_auth', headers={'X-Token': token})
    print(next_res)
    res = web_app.post('/logout')
    next_res = web_app.post('/check_auth', headers={'X-Token': token})
    print(next_res)
    next_res = web_app.post('/check_auth', headers={'X-Token': token})
    print(next_res)

def test_page(web_app):
    token = ".je9YtVbQuBvi65DlkieHGX5l5opM7o24mFcRfp5LLhEVOUSgEGnYLrwx2EOBeSIG2igECbcmw4OX2xFpuhrVPQ"
    next_res = web_app.post('/check_auth', headers={'X-Token': token})
    print(next_res)