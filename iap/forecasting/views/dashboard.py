from ...common.helper import send_success_response, send_error_response
from ..workbench.services import data_management as data_service
from ...common.security import *
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
TOOL = 'forecast'


def get_dashboard_data(req):
    # Get parameters from request.
    try:
        user_id = 2#req.user
    except KeyError as e:
        msg = ErrorManager.get_error_msg(e, 'default')
        return send_error_response(msg)
    try:
        lang = rt.get_state(user_id).language
        project = rt.get_state(user_id)._project_id
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(req, project, wb.container['default'], wb.data_config, wb.selection, lang)
        print("Data", data)
        return send_success_response(data)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


def get_cagrs_for_period(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entities_ids = req.json_body['data']['entities_ids']
        ts = req.json_body['data']['timescale']
        start = req.json_body['data']['start']
        end = req.json_body['data']['end']
    except KeyError as e:
        msg = req.get_error_msg(e, "default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        cagrs = data_service.get_cagrs(wb.container, wb.config, entities_ids, (start, end))
        return send_success_response(cagrs)
    except Exception as e:
        msg = req.get_error_msg(e, "default")
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
    except KeyError as e:
        msg = req.get_error_msg(e, lang="default")
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        dec_data = data_service.get_decomposition(wb.container['default'], wb.config,
                                                    entities_ids, (start, end))
        return send_success_response(dec_data)
    except Exception as e:
        msg = req.get_error_msg(e, "default")
        return send_error_response(msg)







