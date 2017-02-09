import datetime
from ...common.repository.models_managers import scenario_manager as scenario_manager
from ...common.repository.models_managers.access_manager import get_feature_permission
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
from ...common import runtime_storage as rt



@forbidden_view
@requires_roles('Create a new scenario')
def get_scenario_page(request):
    """
    View for url - get scenario page


    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        lang = rt.language(user_id)
        filters = request.json_body['data']['filter']
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        data = scenario_manager.get_scenarios(request, filters)
        #TODO change field of tool_id in db.
        user_permission = get_feature_permission(request, user_id, 1)
        print(user_permission)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        result = {'user_permission': user_permission, "data": data}
        return send_success_response(result)


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
        user_id = request.user
        lang = rt.language(user_id)
        input_data = request.json['data']
        scenario_manager.create_scenario(request, input_data)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
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
        user_id = request.user
        lang = rt.language(user_id)
        filters = request.json_body['data']['filters']
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        scenario_info_list = scenario_manager.get_scenarios(request, filters)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles('View Scenario')
def get_scenario_details(request):
    """
    Return scenario description by given scenario id
    :param request:
    :type request:
    :return:
    :rtype:
    """

    try:
        user_id = request.user
        scenario_id = request.json_body['data']['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        output = scenario_manager.search_and_get_scenarios(request, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e)
        return send_error_response(msg)
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
        user_id = request.user
        scenario_id = request.json_body['data']['scenario_id']
        new_name = request.json_body['data']['name']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        scenario_manager.update_scenario(request, scenario_id, parameter="name", value=new_name)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_success_response(msg)
    else:
        return send_success_response("Name changed")


@forbidden_view
@requires_roles('View Scenario')
def check_scenario_name(request):
    try:
        user_id = request.user
        scenario_id = request.json_body['data']['id']
        name = request.json_body['data']['name']
        value_to_check = {'name': name}
        lang = rt.language(user_id)
        result = scenario_manager.check_scenario(scenario_id, value_to_check)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(result)

@forbidden_view
@requires_roles('Modify Scenario')
def modify(request):
    """Modify scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        new_values = request.json_body['modification_value']
        scenario_id = request.json_body['scenario_id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        updated_scenario = scenario_manager.update_scenario\
            (request, scenario_id, parameter=new_values['parameter'], value=new_values['value'])
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(updated_scenario)


@forbidden_view
@requires_roles('Delete Scenario')
def delete_scenario(request):
    """
    Delete selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        scenario_id = request.json_body['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        scenario_manager.delete_scenario(request, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response("Deleted selected scenario")


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
        user_id = request.user
        scenario_id = request.json_body['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        scenario_manager.update_scenario(request, scenario_id, parameter='status', value="final")
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response("Mark as final")


@forbidden_view
@requires_roles('Include_scenario')
def include_scenario(request):
    try:
        user_id = request.user
        parent_scenario_id = request.json_body['parent_scenario_id']
        scenario_id = request.json_body['scenario_id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        msg = scenario_manager.include_scenario(parent_scenario_id, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
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
