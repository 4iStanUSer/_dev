from ...common.helper import send_success_response, send_error_response
from ..workbench.helper import TOOL
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
from ..workbench.services import data_management as data_service
from ..workbench.helper import Feature
from ...common import runtime_storage as rt


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


def get_simulator_page_data(req):
    """Get data for simulator

    :param req:
    :type req:
    :return:
    :rtype:
    """
    pass


def simulator_custom_data(req):
    """Get simulator custom data

    :param req:
    :type req:
    :return:
    :rtype:
    """

    pass


def get_simulator_decomposition(req):
    """Get simulator decomposition

    :param req:
    :type req:
    :return:
    :rtype:
    """

    pass

def save_scenario(req):
    """
    Save scenario

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = 2#req.get_user
        scenario_id = req.json_body['data']['id']

        state = rt.get_state(user_id)
        lang = state._lang
        wb = rt.get_wb(user_id)


    except KeyError:
        return send_error_response("Key Error")




