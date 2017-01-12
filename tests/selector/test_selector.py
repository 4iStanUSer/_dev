from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('./')
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


def test_selector(token, web_app):
    """
    Test for url get entity selectors config

    :param token:
    :type token:
    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json('/get_options_for_entity_selector', {'X-Token':token})
    print(res)


def test_set_entity_selector(token, web_app):
    """
    Test for url get entity selectors config

    :param token:
    :type token:
    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json('/set_entity_selection', {'X-Token':token})
    print(res)




def test_get_options_entity_selector(web_app):
    """
    Test for url get entity selectors config

    :param token:
    :type token:
    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    token = str(res.json_body['data'])
    print("TOKEN", token)

    res = web_app.post_json('/selector', {'X-Token':token})
    print(res)