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
    res = web_app.post_json('/select_project', {"data": {"project_id": project_id, "tool_id": tool_id},
                                          'X-Token': token})
    print("Select Project")
    print(res.json_body)


    #2.Set value for specific scenario
    values = [dict(var_name="media", timescale="annual", slot_type=1, time_label='1', value=0),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='2', value=0),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='3', value=1),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='4', value=0)
              ]

    scenario_id = "test_scenario_3"
    res = web_app.post_json('/forecast/set_values', {"data": {"entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("Set value for scenario - test_scenario_1")
    print(res.json_body)

    #3.Save scenario
    scenario_id = "test_scenario_3"
    res = web_app.post_json('/forecast/save_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id, "tool_id": tool_id},
                                                        'X-Token': token})
    print("Save scenario - test_scenario_1")
    print(res.json_body)

    #4.Load Scenario
    scenario_id = "test_scenario_3"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id,
                                                                 "tool_id": tool_id},
                                                        'X-Token': token})
    print("Load Scenario - test_scenario")
    print(res.json_body)


    #5.View changes
    res = web_app.post_json('/forecast/get_custom_data', {"data": {"project_id": project_id, "tool_id": tool_id},
                                                          'X-Token': token})

    print("View changes - test_scenario")
    print(res.json_body)
    actual = res.json['data']['annual']['media']['values']
    expected = [0, 0, 0, 1]
    assert actual == expected



