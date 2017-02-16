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
    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=[2012, 2013], value=1110),
              dict(var_name="media", timescale="annual", slot_type=1, time_label=2013, value=1101),
              dict(var_name="media", timescale="annual", slot_type=1, time_label=2014, value=111),
              dict(var_name="media", timescale="annual", slot_type=1, time_label=2015, value=1110)
              ]

    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/set_values', {"data": { "tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("Set value for scenario - test_scenario")
    print(res.json_body)

    #3.Save scenario test_scenario
    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/save_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id, "tool_id": tool_id},
                                                        'X-Token': token})
    print("Save scenario - test_scenario")
    print(res.json_body)

    #4.Load Scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id,
                                                                 "tool_id": tool_id},
                                                        'X-Token': token})
    print("Load Scenario - test_scenario_1")
    print(res.json_body)


    scenario_id = "test_scenario_1"
    #5.Set value for specific scenario test_scenario_1
    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2012, value=1),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2013, value=12),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2014, value=123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label=2015, value=1231)
              ]

    res = web_app.post_json('/forecast/set_values', {"data": {"tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("View changes - test_scenario_1")
    print(res.json_body)

    #6.Save scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/save_scenario',
                            {"data": {"scenario_id": scenario_id, "project_id": project_id, "tool_id": tool_id},
                             'X-Token': token})
    print("Save scenario - test_scenario_1")
    print(res.json_body)



    #7.Load Scenario test_scenario
    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id,
                                                                 "tool_id": tool_id},
                                                        'X-Token': token})

    print("Load Scenario - test_scenario")
    print(res.json_body)


    #8.View changes

    res = web_app.post_json('/forecast/get_custom_data', {"data": {"project_id": project_id, "tool_id": tool_id},
                                                          'X-Token': token})

    print("View changes - test_scenario")
    print(res.json_body)
    actual = res.json['data']['annual']['media']['values']
    expected = [1110, 1101, 111, 1110]
    assert actual == expected

    # 9.Load Scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id, "project_id": project_id,
                                                                 "tool_id": tool_id},
                                                        'X-Token': token})

    print("Load Scenario - test_scenario_1")
    print(res.json_body)

    # 10.Load Scenario test_scenario_1
    res = web_app.post_json('/forecast/get_custom_data', {"data": {"project_id": project_id, "tool_id": tool_id},
                                                          'X-Token': token})

    print("View changes - test_scenario_1")
    print(res.json_body)
    actual = res.json['data']['annual']['eq_price']['values']
    expected = [1, 12, 123, 1231]
    assert actual == expected

