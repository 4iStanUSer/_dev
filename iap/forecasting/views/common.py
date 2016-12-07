from pyramid.renderers import render_to_response
from ..workbench.services import dimensions
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common.helper import send_success_response, send_error_response
from ...common import runtime_storage as rt

def index_view(req):
    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=req)


def get_options_for_entity_selector(req):
    # Get parameters from request.
    try:
        user_id = req.user
        query = req.json_body['query']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        data = dimensions.search_by_query(wb.search_index, query)
        return send_success_response(data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_entity_selectors_config(req):
    try:
        user_id = req.user
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        lang = rt.get_state(user_id).language
        wb = rt.get_wb(user_id)
        selectors_config = \
            dimensions.get_selectors_config(wb.data_config, lang)
        return send_success_response(selectors_config)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)
