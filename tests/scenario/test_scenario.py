from pyramid.paster import get_appsettings
import datetime
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
    res = web_app.post_json('/login', {'data':{"username": login, 'password': password}})
    token = str(res.json_body['data'])

    return token


def test_scenario(web_app, token):
    """
    Test view /get_scenario_list
    :param web_app:
    :type web_app: webtest.app.TestApp
    :param token:
    :type token: str
    :return:
    :rtype: None
    """
    res = web_app.post_json("/forecast/get_scenarios_list", {'X-Token': token})
    actual = res.json
    assert actual['error'] == False
    assert type(actual['data']) == list


def test_create_scenario(web_app, token):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    scenario_data = {
                "name": "New Scenario",
                "description": "New Scenario Description",
                "status": "New",
                "shared": "True",
                "criteria": "USA-Main-Weapon"
                    }

    res = web_app.post_json("/forecast/create_scenario", {"data": scenario_data, "X-Token": token})
    expected = {'data': 'Scenario created', 'error': False}
    actual = res.json
    print("Create Scenario", actual)
    assert expected == actual


def test_search_and_view(web_app, token):
    """Test for get inforamtion about scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    filters = {'authors': [], 'period': [], 'criteria': []}

    res = web_app.post_json("/forecast/search_and_view_scenario", {'filters': filters, 'X-Token': token})
    expected = {"data": [{"id": 1, "status": "New", "shared": 'True', "name": "New Scenario"}], "error": False}
    actual = res.json
    assert expected == actual


def test_get_scenario_details(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 12}, 'X-Token': token})
    expected = {"data": "New Scenario Description", "error": False}
    actual = res.json
    assert actual == expected


def test_change_scenario_name(web_app, token):
    """Test for change sceanrio name

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/change_scenario_name", {"data":
                                                               {'scenario_id': 1, 'name': "New name of Scenario"},
                                                                'X-Token': token})
    actual = res.json
    expected = {"data": "Name changed", "error": False}
    assert actual == expected


def test_publish_scenario(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/publish_scenario", {'id': 1, 'X-Token': token})
    print(res)


def test_mark_as_final_scenario(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/mark_as_final", {'id': 1, 'X-Token': token})
    expected = {'data': 'Mark as final', 'error': False}
    actual = res.json
    print(actual)
    assert expected == actual


def test_include_scenario(web_app, token):
    """Test for get include scenario into hierarchy

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/include_scenario", {'parent_id': 1, "children_id": 3, 'X-Token': token})
    expected = {"error": True, "data": "User 2 Unauthorised"}
    actual = res.json
    assert actual == expected


def test_get_scenario_details(web_app, token):

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 1},'X-Token': token})
    expected =\
    {'data': {'description': 'Dynamics of Price Growth in Brazil', 'id': 1, 'growth_period': '',
              'meta': 'Brazil-Nike-Main',
              'recent_actions': [{'action_name': '', 'entity_id': '', 'action_id': '', 'entity_name': '', 'date': ''}],
              'metrics': [{'name': '', 'value': '', 'format': ''}], 'driver_change': [{'name': '', 'value': ''}],
              'driver_group': [{'name': '', 'value': ''}],
              'worklist': [{'name': 'Price Growth Dynamics JJOralCare', 'id': 1, 'date': '2017_2_7_18_4'}],
              'predefined_drivers': [{'value': '', 'id': ''}]}, 'error': False}

    actual = res.json['data']
    print("Actual", actual)
    assert expected['data']['description'] == actual['description']
    assert expected['data']['meta'] == actual['meta']
    assert expected['data']['id'] == actual['id']


def test_get_scenario_page(web_app, token):

    now = datetime.datetime.now()
    present_time = "{0}_{1}_{2}_{3}_{4}".format(now.year, now.month, now.day, now.hour, now.minute)
    scenario_details = {}

    res = web_app.post_json("/forecast/get_scenario_page", {'data': {'filter': {}},'X-Token': token})
    expected = [
                {"name": "Price Growth Dynamics JJLean",
                 "author": "default_user", "shared": "No", "status": "New",
                 "id": 2, "modify_date": present_time, "location": "New",
                 "description": "Dynamics of Price Growth in USA"}
                ]

    actual = res.json['data']['data']
    print("Actual", actual)
    assert expected[0]['name'] == actual[0]['name']
    assert expected[0]['author'] == actual[0]['author']
    assert expected[0]['id'] == actual[0]['id']
    assert expected[0]['description'] == actual[0]['description']


def test_delete_scenario(web_app, token):
    """Test for delete scenario

    Temprorary disabled

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    #res = web_app.post_json("/forecast/delete_scenario", {'id': 1,  'X-Token': token})
    #expected = {'data': 'Deleted selected scenario', 'error': False}
    #actual = res.json
    #assert expected == actual
