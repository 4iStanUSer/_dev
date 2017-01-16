from ...common.helper import send_success_response, send_error_response
from ..workbench.services import data_management as data_service
from ...common.security import check_permission_for_tool_and_project, check_entities_permission
from ...common.security import *
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
TOOL = 'forecast'


def get_dashboard_data(req):
    # Get parameters from request.
    try:
        user_id = get_user(req).id
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        #check permission for specific data
        #1.workbench
        #2.enities
        lang = rt.get_state(user_id).language
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(wb.container, wb.data_config, wb.selection, lang=lang)
        return send_success_response(data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_cagrs_for_period(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entities_ids = req.json_body['entities_ids']
        ts = req.json_body['timescale']
        start = req.json_body['start']
        end = req.json_body['end']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        if check_entities_permission(req, user_id, entities_ids):
            wb = rt.get_wb(user_id, TOOL)
            cagrs = data_service.get_cagrs(wb.container, wb.config, entities_ids,
                                             (start, end))
            return send_success_response(cagrs)
        #else return - permission error
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_decomposition_for_period(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entities_ids = req.json_body['entities_ids']
        ts = req.json_body['timescale']
        start = req.json_body['start']
        end = req.json_body['end']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        if check_entities_permission(req, user_id, entities_ids):

            wb = rt.get_wb(user_id, TOOL)
            dec_data = data_service.get_decomposition(wb.container, wb.config,
                                                    entities_ids, (start, end))
            return send_success_response(dec_data)
    # else return - permission error
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)







