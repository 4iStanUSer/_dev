from ...common.helper import send_success_response, send_error_response
from ..workbench.services import data_management as data_service
from ...common import runtime_storage as rt
from ...common.repository import persistent_storage
from ...common.repository.models_managers import access_manager

def set_values(req):
    """
    Set value for specific variable
    :param req:
    :type req:
    :return:
    :rtype:
    """
    #try:
    user_id = req.user
    entity_id = req.json_body['data']['entity_id']
    values = req.json_body['data']['values']
    lang = rt.language(user_id)
    #except KeyError as e:
    #msg = req.get_error_message(e, lang)
    #return send_error_response(msg)
    #try:
    wb = rt.get_wb(user_id)
    session = req.dbsession
    project_name = "JJOralCare"
    #TODO Check access to feature.
    #TODO check access for data
    permission_tree = access_manager.build_permission_tree(session=session,project_name=project_name)
    data_service.set_entity_values(permission_tree=permission_tree, container=wb.current_container,
                                   entity_id=entity_id, values=values)
    #except Exception as e:
    #msg = req.get_error_msg(e, lang)
    #return send_error_response(msg)
    #else:
    return send_success_response()


def get_simulator_page_data(req):
    """
    Get data for simulator page
    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = req.user
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_message(e, lang)
        return send_error_response(msg)
    try:
        #TODO check if there are selected scenario
        wb = rt.get_wb(user_id)
        session = req.dbsession
        permission_tree = access_manager.build_permission_tree(session, project_name="JJOral")
        data = data_service.get_simulator_data(session, wb.current_container, wb.data_config,
                                               wb.selection, lang)
        default_data = data_service.get_simulator_value_data(wb.default_container, wb.data_config,  wb.selection, lang)
        data['data']['values']['default'] = default_data
        #TODO change setter of custom data
    except Exception as e:
        msg = req.get_error_msg(e)
        return send_error_response(msg)
    else:
        return send_success_response(data)


def get_simulator_custom_data(req):
    """
    Refresh values of working scenario

    :param req:
    :type req:
    :return:
    :rtype:
    """
    #try:
    user_id = req.user
    lang = rt.language(user_id)
    #except KeyError as e:
    #msg = req.get_error_message(e, lang)
    #return send_error_response(msg)
    #try:
    #TODO check if there are selected scenario
    wb = rt.get_wb(user_id)
    session = req.dbsession
    permission_tree = access_manager.build_permission_tree(session, project_name="JJOral")
    data = data_service.get_simulator_value_data(permission_tree, wb.current_container, wb.data_config, wb.selection, lang=lang)
    #except Exception as e:
    #msg = req.get_error_msg(e)
    #return send_error_response(msg)
    #else:
    return send_success_response(data)


def get_simulator_decomposition(req):
    """Return simulator decomposition
    """
    # Get parameters from request.
    try:
        user_id = req.user
        entities_ids = req.json_body['data']['entities_ids']
        ts_name = req.json_body['data']['timescale']
        start = req.json_body['data']['start']
        end = req.json_body['data']['end']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        dec_data = data_service.get_decomposition(wb.current_container, wb.data_config,
                                                  entities_ids, {ts_name:(start, end)})
        return send_success_response(dec_data)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


def load_scenario(request):
    """
    Load selected scenario
    :param request:
    :type request:
    :return:
    :rtype:
    """
    #TODO Check The Permission for Load and Save Scenario
    try:
        user_id = request.user
        scenario_id = request.json_body['data']['scenario_id']
        project_id = request.json_body['data']['project_id']
        tool_id = request.json_body['data']['tool_id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        backup = persistent_storage.load_backup(user_id, tool_id, project_id, scenario_id)
        wb.load_from_backup(backup, user_access=None, scenario_id=scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    else:
        return send_success_response(scenario_id)


def save_scenario(request):
    """
    Save selected scenario

    :param request:
    :type request:
    :return:
    :rtype:
    """
    # TODO Check The Permission for Load and Save Scenario
    try:
        user_id = request.user
        scenario_id = request.json_body['data']['scenario_id']
        project_id = request.json_body['data']['project_id']
        tool_id = request.json_body['data']['tool_id']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = request.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        # TODO check - if scenario_id in wb.scenario_selection:
        backup = wb.get_backup(cont_type="current")
        persistent_storage.save_backup(user_id, tool_id, project_id, backup, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e)
        return send_error_response(msg, lang)
    else:
        return send_success_response(scenario_id)





