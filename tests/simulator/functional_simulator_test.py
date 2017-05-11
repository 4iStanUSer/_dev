from pyramid.paster import get_appsettings
import pytest
import os
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
    res = web_app.post_json('/select_project', {"data": {"project_id": project_id, "tool_id": tool_id},
                                          'X-Token': token})
    print("Select Project")
    print(res.json_body)


    #2.Set value for specific scenario
    values = [dict(var_name="media", timescale="annual", slot_type=1, time_label='1', value=1110),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='1', value=1101),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='2', value=111),
              dict(var_name="media", timescale="annual", slot_type=1, time_label='3', value=1110)
              ]


    res = web_app.post_json('/forecast/set_values', {"data": { "entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("Set value for scenario - test_scenario")
    print(res.json_body)

    #3.Save scenario test_scenario
    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/save_scenario', {"data": {"scenario_id": scenario_id},
                                                        'X-Token': token})
    print("Save scenario - test_scenario")
    print(res.json_body)

    #4.Load Scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id},
                                                        'X-Token': token})
    print("Load Scenario - test_scenario_1")
    print(res.json_body)


    scenario_id = "test_scenario_1"
    #5.Set value for specific scenario test_scenario_1
    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='1', value=1),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='2', value=12),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='3', value=123),
              dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='4', value=1231)
              ]

    res = web_app.post_json('/forecast/set_values', {"data": {"tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})

    print("View changes - test_scenario_1")
    print(res.json_body)

    #6.Save scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/save_scenario',
                            {"data": {"scenario_id": scenario_id},
                             'X-Token': token})
    print("Save scenario - test_scenario_1")
    print(res.json_body)



    #7.Load Scenario test_scenario
    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id},
                                                        'X-Token': token})

    print("Load Scenario - test_scenario")
    print(res.json_body)


    #8.View changes

    res = web_app.post_json('/forecast/get_custom_data', {"data": {},
                                                          'X-Token': token})

    print("View changes - test_scenario")
    print(res.json_body)
    actual = res.json['data']['annual']['media']['values']
    print("Media Values", actual)
    expected = [0, 1101, 111, 1110]
    assert actual == expected

    # 9.Load Scenario test_scenario_1
    scenario_id = "test_scenario_1"
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id},
                                                        'X-Token': token})

    print("Load Scenario - test_scenario_1")
    print(res.json_body)

    # 10.Load Scenario test_scenario_1
    res = web_app.post_json('/forecast/get_custom_data', {"data": {},
                                                          'X-Token': token})

    print("View changes - test_scenario_1")
    print(res.json_body)
    actual = res.json['data']['annual']['eq_price']['values']
    expected = [5.5514496352576765, 1, 12, 5.762558868192696]
    assert actual == expected

