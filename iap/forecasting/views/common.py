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


def get_selectors_static_config(req):
    #TODO implement function
    mock = {
        'items_title': 'Categories',
        'search_title': 'Search',
        'search_placeholder': 'Type here',
        'search_clear': 'Clear search',
        'selected_title': 'Selected',
        'not_found_items': 'Not found items',
        'apply_button': 'Apply',
        'cancel_button': 'Cancel'
    }
    return send_success_response(mock)

def get_entity_selectors_config(req):
    """
    Get entity selector configuration

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
    try:
        user_id = req.user
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        selectors_config = \
        dimensions.get_selectors_config(wb.data_config, lang)
        return send_success_response(selectors_config)
    except Exception as e:
        msg = req.get_error_message(e, lang)
        return send_error_response(msg)


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
        user_id = req.user
        query = req.json_body['data']['query']
    except KeyError as e:
        send_error_response(e)
    try:
        lang = rt.get_state(user_id).language
        wb = rt.get_wb(user_id)
        if query is None:
            options = dimensions.get_options_by_ents(wb.search_index, wb.selection, lang)
        else:
            options, ents = dimensions.search_by_query(wb.search_index, query)

        return send_success_response(options)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)


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
    try:
        user_id = req.user
        query = req.json_body['data']['query']
        lang = rt.language(user_id)
    except KeyError as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)
    try:
        wb = rt.get_wb(user_id)
        options, ents = dimensions.search_by_query(wb.search_index, query)
        wb.selection = ents
        return send_success_response(options)
    except Exception as e:
        msg = req.get_error_msg(e, lang)
        return send_error_response(msg)