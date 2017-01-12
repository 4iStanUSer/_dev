from pyramid.renderers import render_to_response
from ..workbench.services import dimensions
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common.security import get_user
from ...common.helper import send_success_response, send_error_response
from ...common import runtime_storage as rt

def index_view(req):
    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=req)


def get_entity_selectors_config(req):
    print("Get Entity selection", req)
    try:
        user_id = get_user(req).id
        print("User", user_id)
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        lang = rt.get_state(user_id).language
        print("Lang", lang)
        wb = rt.get_wb(user_id)
        print("WB", wb)
        selectors_config = \
            dimensions.get_selectors_config(wb.data_config, lang)
        print("Selector Config", selectors_config)
        return send_success_response(selectors_config)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_options_for_entity_selector(req):
    # Get parameters from request.
    print("Get options selection", req)
    try:
        user_id = get_user(req).id
        query = req.json_body['data']['query']
        print("User", user_id)
        print("Query", query)
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        print("WB", wb)
        if query is None:
            options = \
                dimensions.get_options_by_ents(wb.search_index, wb.selection)
        else:
            options, ents = dimensions.search_by_query(wb.search_index, query)
        print("Options", options)
        return send_success_response(options)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def set_entity_selection(req):
    # Get parameters from request.
    print("Set Entity Selection", req)
    try:
        user_id = get_user(req).id
        query = req.json_body['data']['query']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        print('WB',wb)
        options, ents = dimensions.search_by_query(wb.search_index, query)
        print('Options', options)
        wb.selection = ents
        print('Ents', ents)
        return send_success_response()
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)