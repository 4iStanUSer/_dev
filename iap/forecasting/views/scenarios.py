import datetime
from ...common.repository.models_managers import scenario_manager
from ...forecasting.services import scenario_service
from ...common.helper import send_success_response, send_error_response
from ...common.security import requires_roles, forbidden_view
from ...common import runtime_storage as rt


@forbidden_view
@requires_roles('view')
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
        session = request.dbsession
        scenarios_page = scenario_service.get_scenario_page(session, user_id=user_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenarios_page)


@forbidden_view
@requires_roles('create')
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
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        scenario = scenario_service.create_scenario(session, user_id=user_id, input_data=input_data)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenario[0])

@forbidden_view
@requires_roles('view')
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
        session = request.dbsession
        scenario_info_list = scenario_service.get_scenarios(session, user_id=user_id, filters=filters)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenario_info_list)


@forbidden_view
@requires_roles('view')
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
    #TODO check_scenario_permission(user_id, scenario_id)
        session = request.dbsession
        output = scenario_service.get_scenario_details(session, user_id=user_id, scenario_id=scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e)
        return send_error_response(msg)
    else:
        return send_success_response(output)


@forbidden_view
@requires_roles('edit')
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
        scenario_id = request.json_body['data']['id']
        new_name = request.json_body['data']['name']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        scenario_service.update_scenario(session, scenario_id=scenario_id, user_id=user_id, parameter="name",
                                         value=new_name)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_success_response(msg)
    else:
        return send_success_response("Name changed")


@forbidden_view
@requires_roles('view')
def check_scenario_name(request):
    try:
        user_id = request.user
        scenario_id = request.json_body['data']['id']
        name = request.json_body['data']['name']
        value_to_check = {'name': name}
        lang = rt.language(user_id)
        result = scenario_manager.check_scenario(scenario_id=scenario_id, value_to_check=value_to_check)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(result)


@forbidden_view
@requires_roles('edit')
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
        scenario_id = request.json_body['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        updated_scenario = scenario_manager.update_scenario\
            (request, scenario_id=scenario_id, parameter=new_values['parameter'], value=new_values['value'])
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(updated_scenario)


@forbidden_view
@requires_roles('delete')
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
        scenarios_id = request.json_body['data']['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        statuses = {}
        session = request.dbsession
        for scenario_id in scenarios_id:
            status = scenario_manager.delete_scenario(session, scenario_id=scenario_id, user_id=user_id)
            statuses[scenario_id]=status
    except TypeError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(statuses)


@forbidden_view
@requires_roles('edit')
def edit_scenario(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        lang = rt.language(user_id)
        scenarios = request.json_body['data']
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        for scenario in scenarios:
            scenario_id = scenario['id']
            for modify_item in scenario['modify']:
                parameter = modify_item['parameter']
                value = modify_item['value']
                scenario_service.update_scenario(session, scenario_id=scenario_id, user_id=user_id, parameter=parameter, value=value)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response("Scenario Edited")


@forbidden_view
@requires_roles('finalize')
def mark_as_final(request):
    """Marks selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        lang = rt.language(user_id)
        scenario_id = request.json_body['data']['id']
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        scenario_service.update_scenario(session, scenario_id=scenario_id, user_id=user_id, parameter='status', value="final")
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response("Mark as final")


@forbidden_view
@requires_roles('modify')
def include_scenario(request):
    try:
        user_id = request.user
        parent_scenario_id = request.json_body['data']['parent_scenario_id']
        scenario_id = request.json_body['data']['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        scenario_manager.include_scenario(session, user_id=user_id,
                                          parent_scenario_id=parent_scenario_id, scenario_id=scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        send_success_response("Scenario Included")


@forbidden_view
@requires_roles('view')
def copy_scenario(request):
    try:
        user_id = request.user
        scenario_id = request.json_body['data']['id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        session = request.dbsession
        scenario = scenario_service.copy_scenario(session, user_id=user_id, scenario_id=scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenario)


@forbidden_view
@requires_roles('view')
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
