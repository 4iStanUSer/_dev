from pyramid.paster import get_appsettings
import datetime
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
    res = web_app.post_json('/login', {'data': {"username": login, 'password': password}})
    token = str(res.json_body['data'])

    return token


def test_edit_scenario_view_updates(web_app, token):
    """Test for change sceanrio name

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    id = 1
    new_name = "New Name"
    res = web_app.post_json("/forecast/edit_scenario", {"data":
                                                               [{'id': id, 'modify':[{'parameter': 'name',
                                                                                     'value': new_name},
                                                                                    {'parameter': 'favorite',
                                                                                     'value': new_name},
                                                                                    {'parameter': 'shared',
                                                                                     'value': new_name},
                                                                                    {'parameter': 'description',
                                                                                     'value': new_name}
                                                                                    ]
                                                                 }],
                                                                'X-Token': token})

    actual = res.json
    expected = {"data": "Name changed", "error": False}
    print("Edit Scenario", actual)

    res = web_app.post_json("/forecast/get_scenario_page",
                            {'data': {'filter': {'name': 'status', 'value': 'New'}}, 'X-Token': token})
    keys = ['data', 'user_permission']
    data_keys = ['author', 'id', 'location', 'modify_date', 'name', 'status', 'shared', 'scenario_permission']
    actual = res.json['data']['data']
    print("Edit Scenario", actual)
    scenario = [i for i in actual if i['id'] == id][0]
    print("Scenario name", scenario)
    assert new_name == scenario['name']
    print("Scenario favorite", scenario['favorite'])
    assert new_name == scenario['favorite']
    print("Scenario shared", scenario['shared'])
    assert new_name == scenario['shared']
    print("Scenario status", scenario['description'])
    assert new_name == scenario['description']


def test_create_scenario(web_app, token):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    name = "New Scenario"
    description = "New Scenario Description"
    criteria = "USA-Main-Weapon"

    scenario_data = {
                "name": "New Scenario",
                "description": "New Scenario Description",
                "criteria": "USA-Main-Weapon"
                    }

    res = web_app.post_json("/forecast/create_scenario", {"data": scenario_data, "X-Token": token})
    expected_error = False
    assert res.json['error'] == expected_error
    actual = res.json['data']

    assert actual['author'] == 'default_user'
    print("Result of  Scenario Creation ", actual['author'])
    assert actual['criteria'] == criteria
    print("Result of  Scenario Creation", actual['criteria'])
    assert actual['description'] == description
    print("Result of  Scenario Creation", actual['description'])
    assert actual['favorite'] == "No"
    print("Result of  Scenario Creation", actual['favorite'])


def test_create_scenario_name_null(web_app, token):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    name = "New Scenario"
    description = "New Scenario Description"
    criteria = "USA-Main-Weapon"

    scenario_data = {
                "name": None,
                "description": "New Scenario Description",
                "criteria": "USA-Main-Weapon"
                    }

    res = web_app.post_json("/forecast/create_scenario", {"data": scenario_data, "X-Token": token})
    expected_error = True
    print("Error Expected ~ Create Scenario with Null name", res.json)
    assert res.json['error'] == expected_error
    actual = res.json['data']

    assert actual == None


def test_create_scenario_error_expected(web_app, token):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    scenario_data = {
                "name": "New Scenario",
                "description": "New Scenario Description",
                "criteria": "USA-Main-Weapon"
                    }

    res = web_app.post_json("/forecast/create_scenario", {"error": scenario_data, "X-Token": token})
    expected = {'data': None, 'error': True}
    actual = res.json
    print("Create Scenario", actual)
    assert expected == actual


def test_create_scenario_check_updates(web_app, token):
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

    web_app.post_json("/forecast/create_scenario", {"error": scenario_data, "X-Token": token})

    filters = {'authors': [], 'period': [], 'criteria': []}

    res = web_app.post_json("/forecast/search_and_view_scenario", {'data':{'filters': filters}, 'X-Token': token})

    actual = [i['name'] for i in res.json['data']]
    print("Create Scenario", actual)
    assert "New Scenario" in actual


def test_search_and_view(web_app, token):
    """Test for get inforamtion about scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    filters = {'authors': ['default_user'], 'period': [], 'criteria': []}

    res = web_app.post_json("/forecast/search_and_view_scenario", {'data':{'filters': filters}, 'X-Token': token})
    expected = {"data": [{"id": 1, "status": "New", "shared": 'True', "name": "New Scenario"}], "error": False}
    actual = res.json
    print("Search and View Scenario Result", actual['data'])
    assert expected['error'] == actual['error']


def test_search_and_view_error_expected(web_app, token):
    """Test for get inforamtion about scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    filters = {'authors': [], 'period': [], 'criteria': []}

    res = web_app.post_json("/forecast/search_and_view_scenario", {'inputs':{'filters': filters}, 'X-Token': token})
    expected = {"data": "Wrong request", "error": True}
    actual = res.json
    print("Search and View Scenario Result", actual)
    assert expected == actual


def test_get_scenario_details(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 4}, 'X-Token': token})
    expected = {"data": "New Scenario Description", "error": False}
    actual = res.json
    assert actual == expected


def test_get_scenario_details_err_expected(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 144}, 'X-Token': token})
    expected = {'data': 'Wrong request', 'error': True}
    actual = res.json
    print("Get Scenario Details Error Expected", actual)
    assert actual == expected


def test_change_scenario_name(web_app, token):
    """Test for change sceanrio name

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/change_scenario_name", {"data":
                                                               {'id': 3, 'name': "New name of Scenario"},
                                                                'X-Token': None})

    actual = res.json

    expected = {"data": "Name changed", "error": False}
    assert actual == expected


def test_change_scenario_name_error_expected(web_app, token):
    """Test for change sceanrio name

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/change_scenario_name", {"data":
                                                                    {'id': 114,
                                                                    'name': "New name of Scenario"},
                                                                'X-Token': token})

    actual = res.json
    expected = {'error': False, 'data': 'Wrong request'}
    print("Name changed error expected", actual)
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
    res = web_app.post_json("/forecast/mark_as_final", {'data': {'id': 3}, 'X-Token': token})
    expected = {'data': 'Mark as final', 'error': False}
    actual = res.json
    print("Mark as final", actual)
    assert expected == actual


def test_mark_as_final_scenario_error_expected(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/mark_as_final", {'id': 3, 'X-Token': token})
    expected = {'data': 'Wrong request', 'error': True}
    actual = res.json
    print("Mark as Final", actual)
    assert expected == actual


def test_mark_as_final_scenario_view_updates(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    web_app.post_json("/forecast/mark_as_final", {'data': {'id': 3}, 'X-Token': token})

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 3}, 'X-Token': token})

    print("Mark as final Updated view", res.json)
    actual = res.json['data']['status']
    expected = "final"
    print("Mark as final Updated view", actual)
    assert expected == actual


def test_include_scenario(web_app, token):
    """Test for get include scenario into hierarchy

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/include_scenario", {'data': {'parent_scenario_id': 3, "scenario_id": 4},
                                                           'X-Token': token})
    expected = {"error": True, "data": "User 2 Unauthorised"}
    print("Include scenario", res.json)
    actual = res.json
    assert actual == expected


def test_get_scenario_details(web_app, token):

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': 3},'X-Token': token})
    expected = \
        {'recent_actions': [{'date': '', 'entity_id': '', 'action_name': '', 'action_id': '', 'entity_name': ''}],
         'driver_change': [{'value': '', 'name': ''}], 'id': 3, 'driver_group': [{'value': '', 'name': ''}],
         'description': 'Dynamics of Price Growth in USA', 'metrics': [{'format': '', 'value': '', 'name': ''}],
         'status': 'final', 'meta': None, 'growth_period': '',
         'worklist': [{'date': '2017_2_14_15_6', 'name': 'New name of Scenario', 'id': 3}]}

    actual = res.json['data']
    print("Actual", actual)
    assert expected['description'] == actual['description']
    assert expected['meta'] == actual['meta']
    assert expected['id'] == actual['id']


def test_get_scenario_page(web_app, token):

    now = datetime.datetime.now()
    present_time = "{0}_{1}_{2}_{3}_{4}".format(now.year, now.month, now.day, now.hour, now.minute)
    res = web_app.post_json("/forecast/get_scenario_page", {'data': {'filter': {'name':'status', 'value':'New'}}, 'X-Token': token})
    keys = ['data', 'user_permission']
    data_keys = ['author', 'id', 'location', 'modify_date', 'name', 'status', 'shared', 'scenario_permission']
    print("Get sceanrio Page", res.json)
    assert sorted(keys) == sorted(list(res.json['data'].keys()))
    assert 'scenario_permission' in sorted(list(res.json['data']['data'][0].keys()))
    assert sorted(data_keys) == sorted(list(res.json['data']['data'][0].keys()))




def _test_delete_scenario_error_expected(web_app, token):
    """Test for delete scenario

    Temprorary disabled

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/delete_scenario", {'data': {'id': 100},  'X-Token': token})
    expected = {'error': True, 'data': 'Wrong request'}
    actual = res.json
    print("Delete Scenario", actual)
    assert expected == actual


def test_copy_scenario_view_updates(web_app, token):
    """Test for delete scenario

    Temprorary disabled

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/get_scenario_page", {'X-Token': token})
    actual = res.json['data']['data']
    print("Get Scenario Page", actual)
    current_length = len(actual)
    scenario = [i for i in actual if i['id'] == 1][0]
    print("Scenario", scenario)
    criteria = scenario['criteria']
    description = scenario['description']
    favorite = scenario['favorite']

    res = web_app.post_json("/forecast/copy_scenario", {'data': {'id': 1},  'X-Token': token})
    actual = res.json['data']
    print("Copied Scenario", actual)

    #assert actual['author'] == 'default_user'
    print("Result of  Scenario Creation ", actual['author'])
    assert actual['criteria'] == criteria
    print("Result of  Scenario Creation", actual['criteria'])
    assert actual['description'] == description
    print("Result of  Scenario Creation", actual['description'])
    assert actual['favorite'] == favorite
    print("Result of  Scenario Creation", actual['favorite'])


    res = web_app.post_json("/forecast/get_scenario_page", {'data': {'filter': []},'X-Token': token})
    expected_error =  False
    actual = res.json['data']['data']
    print("copy Scenario View Updates", actual)
    assert expected_error == False
    assert len(actual)==current_length+1



def _test_delete_scenario_view_updates(web_app, token):
    """Test for delete scenario

    Temprorary disabled

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/delete_scenario", {'data': {'id': [1, 2, 3, 4, 5, 6, 3]},  'X-Token': token})
    actual = res.json
    print("Delete Scenario", actual)

    res = web_app.post_json("/forecast/get_scenario_details", {'data': {'id': [3]}, 'X-Token': token})
    expected = {'error': True, 'data': 'Wrong request'}
    actual = res.json
    print("Delete Scenario View Updates", actual)
    assert expected == actual