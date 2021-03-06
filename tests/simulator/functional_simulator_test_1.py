from pyramid.paster import get_appsettings
from sqlalchemy.orm.exc import NoResultFound
import pytest
import os
import json
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
    scenario_id = "test_scenario_2"

    res = web_app.post_json('/select_project', {"data": {"project_id": project_id, "tool_id": tool_id},
                                          'X-Token': token})
    print("Select Project")
    print(res.json_body)


    #2.Set value for Specific Variables

    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='0', value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='1', value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='2', value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='3', value=1),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='4', value=1)]

    res = web_app.post_json('/forecast/set_values', {"data": {"tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("Set Value for Specific Variables")
    print(res.json_body)


    #3.View changes

    res = web_app.post_json('/forecast/get_custom_data', {"data": {},
                                                          'X-Token': token})

    actual = res.json['data']['annual']['eq_price']['values']

    expected = [5.5514496352576765, 1123123123, 1123123123, 5.762558868192696]
    print("View changes")
    print(actual)
    assert actual == expected

