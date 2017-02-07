from ...common.helper import send_success_response, send_error_response
from ..workbench.services import data_management as data_service
from ...common import runtime_storage as rt
from ...common.repository import persistent_storage


def set_values(req):
    """
    Set value for specific variable
    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = 2#TODO change on req.get_user
        entity_id = req.json_body['data']['entity_id']
        values = req.json_body['data']['values']
    except KeyError as e:
        msg = req.get_error_message(e, lang="default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        #TODO Check access to feature.
        #TODO check access for data
        data_service.set_entity_values(wb.current_container, entity_id, values)
    except Exception as e:
        msg = req.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
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
        user_id = 2#TODO change on req.get_user
    except KeyError as e:
        msg = req.get_error_message(e, lang="default")
        return send_error_response(msg)
    try:
        #TODO check if there are selected scenario
        wb = rt.get_wb(user_id)
        lang = rt.get_state(user_id).language
        data = data_service.get_simulator_data(req, wb.current_container, wb.data_config, wb.selection,
                                               lang)
    except Exception as e:
        msg = req.get_error_msg(e, lang="default")
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
    try:
        user_id = 2#TODO change on req.get_user
    except KeyError as e:
        msg = req.get_error_message(e, lang="default")
        return send_error_response(msg)
    try:
        #TODO check if there are selected scenario
        wb = rt.get_wb(user_id)
        lang = rt.get_state(user_id).language
        data = data_service.get_simulator_custom_data(wb.current_container, wb.data_config, wb.selection,
                                                      lang)
    except Exception as e:
        msg = req.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(data)


def get_simulator_decomposition(req):
    """Return simulator decomposition
    """
    # Get parameters from request.
    try:
        user_id = 2#TODO change on req.get_user
        entities_ids = req.json_body['data']['entities_ids']
        ts_name = req.json_body['data']['timescale']
        start = req.json_body['data']['start']
        end = req.json_body['data']['end']
    except KeyError as e:
        msg = req.get_error_msg(e, "default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        dec_data = data_service.get_decomposition(wb.current_container, wb.data_config,
                                                  entities_ids, {ts_name:(start, end)})
        return send_success_response(dec_data)
    except Exception as e:
        msg = req.get_error_msg(e, "default")
        return send_error_response(msg)


def get_simulator_data(request):
    """Get data for simulator

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = 2#TODO change on req.get_user
        lang = rt.get_state(user_id).language
        project = rt.get_state(user_id)._project_id
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(request, project, wb.current_container, wb.data_config,
                                            wb.selection, lang)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(data)


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
        user_id = 2#TODO change on req.get_user
        scenario_id = request.json_body['data']['scenario_id']
        project_id = request.json_body['data']['project_id']
        tool_id = request.json_body['data']['tool_id']
    except KeyError:
        return send_error_response("Failed to load scenario")
    try:
        wb = rt.get_wb(user_id)
        backup = persistent_storage.load_backup(user_id, tool_id, project_id, scenario_id)
        wb.load_from_backup(backup, user_access=None, scenario_id=scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
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
        user_id = 2#TODO change on req.get_user
        scenario_id = request.json_body['data']['scenario_id']
        project_id = request.json_body['data']['project_id']
        tool_id = request.json_body['data']['tool_id']
    except KeyError as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        # TODO check - if scenario_id in wb.scenario_selection:
        backup = wb.get_backup(cont_type="current")
        persistent_storage.save_backup(user_id, tool_id, project_id, backup, scenario_id)
    except Exception as e:
        msg = request.get_error_msg(e, lang="default")
        return send_error_response(msg)
    else:
        return send_success_response(scenario_id)





