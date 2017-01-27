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


def test_main_page(web_app):
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    print(res)
    token = str(res.json_body['data'])

    res = web_app.post_json('/check_auth', {'X-Token': token})
    expected = {"data": token, "error": False}
    actual = res.json
    print(actual)
    assert actual == expected


def test_login(web_app):
    """"""
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    print(res)


def test_login_exception_non_existend(web_app):

    login = "username"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    expected = {'data': 'Unauthorised', 'error': True}
    actual = res
    assert expected == actual.json


def test_check_auth(web_app):
    """
    {'login': 'default_user', 'password': '123456', 'id'=1}

    :param web_app:
    :type web_app:
    :return:
    :rtype:

    """
    token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImxvZ2luIjoiZGVmYXVsdF91c2VyIiwiaWF0IjoxNDgxNzk0MjI5fQ.mW8JQOAbnFxDFVBmt5RznYmrVaqdoQIRmUDtCZ6r7KcixsiBWYB6JaCF3SXgZg6nt8kmzEULwT2B5n18R1OaTg"
    res = web_app.post_json('/check_auth', {'X-Token': token})
    print(res)


def test_check_auth_non_existet_user(web_app):
    """
    {'login': 'unexisted_user', 'password': '123456', 'id'=10}

    :param web_app:
    :type web_app:
    :return:
    :rtype:

    """
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbiI6InVuZXhpc3RlZF91c2VyIiwic3ViIjoxMCwiaWF0IjoxNDgxNzk1OTcyfQ.zXdgnG8ouQIf38aMg3166jx9FKlxDcNqzqzfl6ibsdoZd7CgQ6JPzjFgOaYRNxtYkerRrQoj8Hbm243XqdzFiA"
    res = web_app.post_json('/check_auth', {'X-Token': token})
    expected = {"error": True, "data": "Unauthorised"}
    actual = res.json
    assert expected == actual


def test_login_wrong_head(web_app):
    res = web_app.post_json('/login')
    expected = {"error": True, "data": "Unauthorised"}
    actual = res.json
    assert expected == actual


def test_login_wrong_value(web_app):
    token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImxvZ2luIjoiZGVmYXVsdF91c2VyIiwiaWF0IjoxNDgxNzk0MjI5fQ.mW8JQOAbnFxDFVBmt5RznYmrVaqdoQIRmUDtCZ6r7KcixsiBWYB6JaCF3SXgZg6nt8kmzEULwT2B5n18R1OaTg"
    res = web_app.post_json('/check_auth', {'X-Token': token})
    print(res)


def test_first_step_authentification(web_app):

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOjEsImlhdCI6MTQ4MTcyNjc4NSwibG9naW4iOiJsZW9uaWRkaWR1a2gifQ.uHLOtwNOxATfjbQX0AQL__rH1evj_76T000AV7UnLPkagK1dMD39S-ldWBxklNEHysnc6JU4EZkt6J4IewumLg"
    res = web_app.post('/routing_config', {'X-Token': token})
    print(res)


def test_second_step_authentification(web_app):

    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {'data':{"username": login, 'password': password}})
    token = str(res.json_body['data'])
    res = web_app.post_json('/check_auth', {'X-Token': token})

    expected = {"data": token, "error": False}
    actual = res.json
    assert actual == expected
