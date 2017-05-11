from pyramid.paster import get_appsettings
from sqlalchemy.orm.exc import NoResultFound
import pytest
import os
import json
from iap import main

ABS_PATH = os.path.abspath('./')


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


@pytest.fixture
def token(web_app):
    """
    Fixture produce token for authentification

    :param web_app:
    :type web_app: webtest.app.TestApp
    :return:
    :rtype: str
    """

    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    token = str(res.json_body['data'])

    return token


def test_simulator_functionally(web_app, token):
    """
    Test save scenario

    :param web_app:
    :type web_app:
    :param token:
    :type token:
    :return:
    :rtype:
    """

    #1.Select Project

    project_id = 'JJOralCare'
    tool_id = 'forecast'
    res = web_app.post_json('/select_project', {"data": {"project_id": project_id, "tool_id": tool_id},
                                          'X-Token': token})



    res = web_app.post_json('/forecast/get_options_for_entity_selector', {"data": {"query": None},
                                                'X-Token': token})
    print("Select Project")
    print(res.json_body)