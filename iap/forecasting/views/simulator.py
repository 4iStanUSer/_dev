from ...common.helper import send_success_response, send_error_response
from ..workbench.helper import TOOL
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
from ..workbench.services import data_management as data_service
from ..workbench.helper import Feature


def set_values(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entity_id = req.json_body('entity_id')
        values = req.json_body('values')
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id, TOOL)
        # Check access to feature.
        if not wb.access.check_feature_access(Feature.edit_values):
            raise Exception
        data_service.set_entity_values(wb, entity_id, values)
        return send_success_response()
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
    return send_error_response(msg)
