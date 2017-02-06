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


def test_save_scenario(web_app, token):
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


    #2. Save Scenario

    scenario_id = "test_scenario"
    res = web_app.post_json('/forecast/save_scenario', {"data": {"scenario_id": scenario_id, "tool_id": tool_id},
                                                        'X-Token': token})



    #3.Set value for specific variables

    scenario_id = "test_scenario"
    values = [dict(var_name="eq_price", timescale="annual", slot_type=1, time_label='2014', value=222222)]
    res = web_app.post_json('/forecast/set_values', {"data": {"scenario_id": scenario_id, "tool_id": tool_id,
                                                              "entity_id": 12, "values": values},
                                                     "X-Token": token})

    #4.Update page
    res = web_app.post_json('/forecast/get_simulator_data', {"data": {"project_id": project_id,
                                                                      "tool_id": tool_id}, 'X-Token': token})

    # 4.Update page

    res = web_app.post_json('/forecast/get_simulator_page_data', {"data": {"project_id": project_id,
                                                                           "tool_id": tool_id}, 'X-Token': token})

    print("Get Simulator Page Data Actual", res.json['data']['data']['values']['annual']['eq_price'])


    #5. Save changes
    res = web_app.post_json('/forecast/save_scenario', {"data": {"scenario_id": scenario_id, "tool_id": tool_id},
                                                        'X-Token': token})

    # 5. Load changes
    res = web_app.post_json('/forecast/load_scenario', {"data": {"scenario_id": scenario_id,
                                                                 "tool_id": tool_id}, "X-Token": token})

    #6 View changes
    res = web_app.post_json('/forecast/get_simulator_page_data', {"data": {"project_id": project_id,
                                                                           "tool_id": tool_id}, 'X-Token': token})

    assert res.json['data']['data']['values']['annual']['eq_price'][1] == 222222