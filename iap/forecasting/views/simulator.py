from ...common.helper import send_success_response, send_error_response
from ..workbench.helper import TOOL
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import runtime_storage as rt
from ..workbench.services import data_management as data_service
from ..workbench.helper import Feature
from ...common import runtime_storage as rt
from ...common.repository import persistent_storage


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


def get_simulator_page_data(request):
    """Get data for simulator

    :param req:
    :type req:
    :return:
    :rtype:
    """
    try:
        user_id = 2
        tool_id = "forecast"
        lang = rt.get_state(user_id).language
        project = rt.get_state(user_id)._project_id
        wb = rt.get_wb(user_id)
        data = data_service.get_entity_data(request, project, wb.container['current'], wb.data_config, wb.selection, lang)
        return send_success_response(data)
        return send_error_response("Failed to save scenario description")
    except KeyError:
        return send_error_response("Failed to save scenario description")
    else:
       return send_success_response(scenario_id)


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


def load_scenario(request):
    #Check The Permission for Load and Save Scenario
    try:
        user_id = 2
        scenario_id = request.json_body['data']['scenario_id']
        project_id = "JJOralCare" #rt.get_state(user_id)._project_id
        tool_id = "forecast"

        data = rt._load_scenario(user_id, tool_id, project_id, scenario_id)
    except KeyError:
        return send_error_response("Failed to load scenario")
    else:
        return send_success_response(data)


def save_scenario(request):
    # Check The Permission for Load and Save Scenario
    try:
        user_id = 2
        scenario_id = request.json_body['data']['scenario_id']
        project_id = "JJOralCare"#rt.get_state(user_id)._project_id
        tool_id = "forecast"
    #if scenario_id not in wb.scenario_selection:
    #    pass
    #else:
        rt._save_scenario(user_id, tool_id, project_id, scenario_id)
        return send_success_response(scenario_id)
    except KeyError:
        return send_error_response("Failed to save scenario description")
    else:
       return send_success_response(scenario_id)






