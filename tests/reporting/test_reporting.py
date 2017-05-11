import pytest
import os
import json
import pyramid.httpexceptions as httpexc
from pyramid.paster import get_appsettings
from iap import main

ABS_PATH = os.path.abspath('./')


@pytest.fixture
def web_app():
    """Fixture for server preparation

    :return:
    :rtype: webtest.app.TestApp
    """
    settings = get_appsettings(os.path.join(ABS_PATH, 'test.ini'), name='main')
    app = main(global_config=None, **settings)
    from webtest import TestApp
    test_app = TestApp(app)
    return test_app


@pytest.fixture
def token(web_app):
    """Fixture produce token for authentication

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


def test_get_report_options(web_app, token):
    """Test for view get_report_options

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    data = web_app.post_json("/forecast/get_report_options", headers={'X-Token': token})
    actual = json.loads(data.json)
    expected = json.loads(open('tests/reporting/json/report_options.json').read())
    assert actual == expected


def test_get_report_options_exception_401(web_app):
    """Test for view get_report_options exception 401

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    with pytest.raises(Exception) as exc_info:
        web_app.post_json("/forecast/get_report_options")
    actual = exc_info.value.args[0]
    expected = httpexc.HTTPUnauthorized().status
    assert expected in actual


def test_generate_report(web_app, token):
    """Test for view generate_report

    :param web_app:
    :type web_app:
    :return:
    :rtype:
    """
    data = web_app.post_json("/forecast/generate_report", {'data': {'project': 'JJOralCare', 'file_name': None}},
                             headers={'X-Token': token})
    actual = json.loads(data.json)
    expected = 'Success'
    assert actual == expected












# TODO create_report(file_name, report_data_list)
# TODO data_to_table(section, time_labels, variable_values, variables):🐈

