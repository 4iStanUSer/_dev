from ...common.helper import send_success_response, send_error_response
from ..workbench.services import data_management as data_service
from ...common.security import *
from ...common.repository.models_managers.access_manager import build_permission_tree
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
TOOL = 'forecast'


def get_dashboard_data(req):
    # Get parameters from request.
    # try:
    user_id = req.user
    lang = rt.language(user_id)
    #except KeyError as e:
    #    msg = ErrorManager.get_error_msg(e, lang)
    #    return send_error_response(msg)
    #try:
    lang = rt.get_state(user_id).language
    project = rt.get_state(user_id)._project_id
    wb = rt.get_wb(user_id)
    session = req.dbsession
    permission_tree = build_permission_tree(session, project_name=project)
    wb.selection = [9]
    data = data_service.get_entity_data(permission_tree, project, wb.default_container, wb.data_config,
                                wb.selection, lang)
    return send_success_response(data)
    #except Exception as e:
    #    msg = req.get_error_msg(e, lang)
    #    return send_error_response(msg)


def get_cagrs_for_period(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entities_ids = req.json_body['data']['entities_ids']
        ts = req.json_body['data']['timescale']
        start = req.json_body['data']['start']
        end = req.json_body['data']['end']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        cagrs = data_service.get_cagrs(wb.default_container, wb.config, entities_ids, (start, end))
        return send_success_response(cagrs)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


def get_decomposition_for_period(req):
    """
    Return decomposition data for period

    :param req:
    :type req:
    :return:
    :rtype:
    """
    # Get parameters from request.
    try:
        user_id = req.get_user
        entities_ids = req.json_body['data']['entities_ids']
        ts = req.json_body['data']['timescale']
        start = req.json_body['data']['start']
        end = req.json_body['data']['end']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        dec_data = data_service.get_decomposition(wb.container['default'], wb.config,
                                                    entities_ids, (start, end))
        return send_success_response(dec_data)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)







