import datetime
from ...common.repository.models_managers.scenario import create_scenario, get_scenarios, \
    update_scenario, check_scenario, delete_scenario, search_and_get_scenarios

from iap.common.repository.models.scenarios import Scenario
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view


def create_table(request):
    """
    Create Scenario Table
    :param request:
    :type request:
    :return:
    :rtype:
    """
    from iap.common.repository.db.meta import Base
    _engine = request.dbsession.bind.engine
    # Create all tables
    Base.metadata.create_all(_engine)


def prepare_scenario_testing(request):
    """
    Prepare db for testing
    :param request:
    :type request: pyramid.util.Request
    :return:
    :rtype: None
    """

    scenarios = request.dbsession.query(Scenario).all()
    for scenario in scenarios:
        request.dbsession.delete(scenario)


def serialise_scenario(scenarios):
    """
    Serialise scenario into dictionary
    :param scenarios:
    :type scenarios:
    :return:
    :rtype:
    """
    scenario_info_list = []
    scenario_info = {}
    for scenario in scenarios:
        scenario_info['id'] = scenario.id
        scenario_info['name'] = scenario.name
        scenario_info['status'] = scenario.status
        scenario_info['shared'] = scenario.shared
        scenario_info_list.append(scenario_info)
    return scenario_info_list




def get_scenario_page_data():
    pass


def get_sceanrio_details(sceanrio_id):
    pass


def set_scenario_location(location_id):
    pass

def set_scenario_sta

@forbidden_view
@requires_roles('Create a new scenario')
def create_scenario(request):
    """Function for creating new scenario
    args:
        scenario name
        scenario description
        geographies that scenario encompass
        product that scenario encompass
        chanell that scenario encompass
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        input_data = request.json_body['data']
        create_scenario(input_data)
    except KeyError:
        return send_error_response("Failed to create scenario")
    else:
        return send_success_response("Scenario created")


@forbidden_view
@requires_roles('View Scenario')
def search_and_view_scenario(request):
    """
    Return list of scenario by given filters

    :param request:
    :type request:
    :param kwarg:
    :type kwarg:
    :return:
    :rtype:
    """
    try:
        filters = request.json_body['data']['filters']
        scenario_info_list = get_scenarios(request, filters)
    except KeyError:
        return send_error_response("Error during searching")
    else:
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles('View Scenario')
def get_scenario_description(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        output = search_and_get_scenarios(scenario_id, 'description')
    except KeyError:
        return send_error_response("Failed to get scenario description")
    else:
        return send_success_response(output)


@forbidden_view
@requires_roles('View Scenario')
def change_scenario_name(request):
    """
    Change scenario name

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        new_name = request.json_body['data']['new_name']
        new_value = {"name": new_name}
        update_scenario(request, scenario_id, new_value)
    except KeyError:
        return send_error_response("Failed to change name")
    else:
        return send_success_response("Name changed")


@forbidden_view
@requires_roles('View Scenario')
def check_scenario_name(request):
    try:
        scenario_id = request.json_body['data']['id']
        name = request.json_body['data']['name']
        value_to_check = {'name': name}
        result = check_scenario(scenario_id, value_to_check)
        if result:
            return send_success_response("Name checked")
    except KeyError:
        return send_error_response("Failed to check name")
    else:
        return send_error_response("Failed to check name")


@forbidden_view
@requires_roles('Modify Scenario')
def modify(request):
    """
    Modify scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        new_values = request.json_body['data']['modification_value']
        scenario_id = request.json_body['data']['scenario_id']
        update_scenario(request, scenario_id, new_values)
    except KeyError:
        return send_error_response("Failed to modify selected scenario")
    else:
        return send_success_response(update_scenario)


@forbidden_view
@requires_roles('Delete Scenario')
def delete(request):
    """
    Delete selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        delete_scenario(request, scenario_id)
    except KeyError:
        return send_error_response("Failed to delete selected scenario")
    else:
        return send_success_response("Deleted selected scenario")


@forbidden_view
@requires_roles('Publish Scenario')
def publish_scenario(request):
    """Publish selected scenario to central repository
    :param request:
    :type request:
    :return:
    :rtype:
    """
    pass


@forbidden_view
@requires_roles('View Scenario')
def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['data']['id']
        new_value = {'status': 'final'}
        update_scenario(request, scenario_id, new_value)
    except:
        return send_error_response("Marking as final failed")
    else:
        return send_success_response("Mark as final")


@forbidden_view
@requires_roles('Include_scenario')
def include_scenario(request):

    try:
        parent_scenario_id = request.json_body['data']['parent_scenario_id']
        scenario_id = request.json_body['data']['scenario_id']
        msg = include_scenario(parent_scenario_id, scenario_id)
    except KeyError:
        return send_error_response(msg)
    else:
        send_success_response(msg)


@forbidden_view
@requires_roles('View Scenario')
def get_scenarios_list(request):
    scenarios = [
        {
            'id': 1,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 2,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': True,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 3,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 4,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        },
        {
            'id': 5,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 6,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 7,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 8,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        }
    ]

    return send_success_response(scenarios)
