from pyramid.paster import get_appsettings
import pytest
import os
import json
from iap import main
ABS_PATH = os.path.abspath('../')
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
    login = "default_user"
    password = "123456"
    res = web_app.post_json('/login', {"username": login, 'password': password})
    token = str(res.json_body['data'])
    return token

def setup_module():
    server = web_app()
    res = server.post_json("/test_preparation", {'test_name': "scenario"})
    print(res)


def test_scenario(web_app, token):

    res = web_app.post_json("/forecast/get_scenarios_list", {'X-Token': token})
    print(res)


def test_create_scenario(web_app, token):
    """Test for create scenario

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    scenario_data = {
                "name": "New Scenario",
                 "description": "new scenario description",
                 "status": "New",
                 "shared": "True",
                 "geographie": "USA",
                 "product": "Weapon",
                 "channel": "Main",
                 "X-Token": token
                    }

    res = web_app.post_json("/forecast/create_scenario", scenario_data)
    expected = {'data': 'Scenario created', 'error': False}
    actual = res.json
    assert expected == actual


def test_search_and_view(web_app, token):
    """Test for get scenario description

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


def test_get_scenario_description(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/get_scenario_description", {'id': 1, 'X-Token': token})
    expected = {"data": "new scenario description", "error": False}
    actual = res.json
    assert actual == expected


def test_change_scenario_name(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/change_scenario_name", {'id': 1, 'new_name': "New name of Scenario",
                                        'X-Token': token})
    print(res)


def test_publish_scenario(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    res = web_app.post_json("/forecast/publish", {'id': 1})
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
    assert expected == actual


def test_include_scenario(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/mark_as_final", {'parent_id': 1, "children_id": 3, 'X-Token': token})
    print(res)


def test_delete_scenario(web_app, token):
    """Test for get scenario description

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """

    res = web_app.post_json("/forecast/delete_scenario", {'id': 1,  'X-Token': token})
    expected = {'data': 'Deleted selected scenario', 'error': False}
    actual = res.json
    assert expected == actual