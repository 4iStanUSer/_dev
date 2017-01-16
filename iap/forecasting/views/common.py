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
    """
    Get entity selection configuration

    Get Selector Config

    Now Return
    Selector Config {'order': ['geography', 'products', 'market'],
                    'selectors':
                                {'geography':
                                {'multiple': '1', 'name': 'geography', 'disabled': False,
                                 'type': 'flat', 'placeholder': 'geography', 'icon': ''}}}
    :param req:
    :type req:
    :return:
    :rtype:
    """
    print("Get entity selector config")
    try:
        user_id = get_user(req).id
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    #try:
    lang = rt.get_state(user_id).language
    wb = rt.get_wb(user_id)
    selectors_config = \
        dimensions.get_selectors_config(wb.data_config, lang)
    print("Selector Config", selectors_config)
    return send_success_response(selectors_config)
    #except Exception as e:
    #    msg = ErrorManager.get_error_message(e)
    #    return send_error_response(msg)


def get_options_for_entity_selector(req):
    """
    View for get_options for entity selectors

    Args:
        user_id
        query - dictionary with dimension and options
    :param req:
    :type req:
    :return:
    :rtype:
    """
    # Get parameters from request.
    #check permission for workbecnh -- for project and tool

    try:
        user_id = get_user(req).id
        query = req.json_body['data']['query']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    #try:
    lang = rt.get_state(user_id).language
    wb = rt.get_wb(user_id)

    if query is None:
        options = dimensions.get_options_by_ents(wb.search_index, wb.selection, lang)
    else:
        options, ents = dimensions.search_by_query(wb.search_index, query)
    print("Get options for entity selection", options)
    return send_success_response(options)
#    except Exception as e:
#       msg = ErrorManager.get_error_message(e)
#      return send_error_response(msg)


def set_entity_selection(req):
    # Get parameters from request.
    """
    View function for url /set_entity_selection

    From request get query (Dict) - dimension, value

    Add logic - if query is None

    :param req:
    :type req:
    :return:
    :rtype:
    """
    print("Set Entity Selection")
    try:
        user_id = get_user(req).id
        query = req.json_body['data']['query']

    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    #try:

    wb = rt.get_wb(user_id)
    print('WB', wb)
    options, ents = dimensions.search_by_query(wb.search_index, query)
    wb.selection = ents
    print("Selected Opt", options)
    print("Selected", ents)
    return send_success_response()
    #except Exception as e:
    #    msg = ErrorManager.get_error_message(e)
    #    return send_error_response(msg)