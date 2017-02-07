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
    res = web_app.post_json('/login', {'data': {"username": login, 'password': password}})
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
    print(res.json_body)


    #2.Set value for specific variables

    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2012, value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2012, value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2013, value=1123123123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2014, value=1),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2015, value=1)]

    res = web_app.post_json('/forecast/set_values', {"data": {"tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})
    print(res.json_body)


    #3.View changes

    res = web_app.post_json('/forecast/get_custom_data', {"data": {"project_id": project_id, "tool_id": tool_id},
                                                          'X-Token': token})

    actual = res.json['data']['data']['values']['annual']['eq_price']
    expected = [1123123123, 1123123123, 1, 1]
    print(actual)

    assert actual == expected

