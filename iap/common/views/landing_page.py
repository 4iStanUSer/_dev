from ..helper_lib import send_success_response, send_error_response
from ..run_time_storage import State
from ..error_manager import ErrorManager
from ...common import exceptions as ex
from ...common import rt_storage

from pyramid.renderers import render_to_response

def get_tools_list(req):
    # TODO add realization (DR)
    data = dict(forecast=dict(name='Forecasting Tool',
                              projects=[
                                  dict(id='JJOralCare', name='JJ Oral Care'),
                                  dict(id='JJLean', name='JJ Lean Forecasting')
                              ]))
    return send_success_response(data)


def set_tool_selection(req):
    state = State()
    try:
        state.user_id = req.json_body['user_id']
        state.tool_id = req.json_body['tool_id']
        state.project_id = req.json_body['project_id']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        rt_storage.set_state(state)
        return send_success_response()
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


