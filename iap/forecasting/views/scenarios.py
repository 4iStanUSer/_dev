import datetime
from ...common.repository.models_managers.scenario import create_scenario, get_scenarios, \
    update_scenario, check_scenario, delete_scenario, search_and_get_scenarios, serialise_scenario
from ...common.repository.models_managers import scenario as scenario_manager
from ...common.security import get_feature_permission
from ..workbench.services import data_management as data_service
from iap.common.repository.models.scenarios import Scenario
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
from ...common import runtime_storage as rt



#@forbidden_view
#@requires_roles('Create a new scenario')
def get_scenario_page(req):
    """
    View for url - get scenario page


    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        filters = req.json_body['data']['filter']
        author = 2# ToDo change on req.get_user
    except KeyError as e:
        msg = req.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        data = scenario_manager.get_scenarios(req, filters, author)
        user_permission = get_feature_permission(req, author, "forecast")
    except Exception as e:
        msg = req.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        result = {'user_permission': user_permission, "data": data}
        return send_success_response(result)


#@forbidden_view
#@requires_roles('Create a new scenario')
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
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response("Scenario created")


def set_scenario_selection(req):
    pass


#@forbidden_view
#@requires_roles('View Scenario')
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
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        scenario_info_list = get_scenarios(request, filters)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(scenario_info_list)


#@forbidden_view
#@requires_roles('View Scenario')
def get_scenario_details(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """

    try:
        scenario_id = request.json_body['data']['id']
        output = search_and_get_scenarios(request, scenario_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        output = search_and_get_scenarios(request, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(output)


#@forbidden_view
#@requires_roles('View Scenario')
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
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        update_scenario(request, scenario_id, new_value)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_success_response(msg)
    else:
        return send_success_response("Name changed")


def set_scenario_selection(request):
    """
    Set selection function

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = 2#TODO request.get_user
        scenario_id = request.json_body['data']['id']
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        lang = rt.get_state(user_id).language
        project = rt.get_state(user_id)._project_id
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(request, project, wb.container['current'],
                                            wb.data_config, wb.selection, lang)
        return send_success_response(data)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)


#@forbidden_view
#@requires_roles('View Scenario')
def check_scenario_name(request):
    try:
        scenario_id = request.json_body['data']['id']
        name = request.json_body['data']['name']
        value_to_check = {'name': name}
        result = check_scenario(scenario_id, value_to_check)
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(result)

#@forbidden_view
#@requires_roles('Modify Scenario')
def modify(request):
    """Modify scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        new_values = request.json_body['modification_value']
        scenario_id = request.json_body['scenario_id']
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        updated_scenario = update_scenario(request, scenario_id, new_values)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(updated_scenario)


#@forbidden_view
#@requires_roles('Delete Scenario')
def delete(request):
    """
    Delete selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['id']
        delete_scenario(request, scenario_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response("Deleted selected scenario")


#@forbidden_view
#@requires_roles('View Scenario')
def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        scenario_id = request.json_body['id']
        new_value = {'status': 'final'}
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        update_scenario(request, scenario_id, new_value)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response("Mark as final")


#@forbidden_view
#@requires_roles('Include_scenario')
def include_scenario(request):
    try:
        parent_scenario_id = request.json_body['parent_scenario_id']
        scenario_id = request.json_body['scenario_id']
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        msg = include_scenario(parent_scenario_id, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        send_success_response(msg)


#@forbidden_view
#@requires_roles('View Scenario')
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
