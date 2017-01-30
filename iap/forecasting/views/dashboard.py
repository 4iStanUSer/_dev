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
        user_id = req.user
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        lang = rt.get_state(user_id).language
        project = rt.get_state(user_id)._project_id
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(req, project, wb.container['default'], wb.data_config, wb.selection, lang)
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
        wb = rt.get_wb(user_id, TOOL)
        cagrs = data_service.get_cagrs(wb.container, wb.config, entities_ids,
                                         (start, end))
        return send_success_response(cagrs)
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
        wb = rt.get_wb(user_id, TOOL)
        dec_data = data_service.get_decomposition(wb.container, wb.config,
                                                    entities_ids, (start, end))
        return send_success_response(dec_data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)







