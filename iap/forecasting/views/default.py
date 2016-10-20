from pyramid.renderers import render_to_response

from ...common.helper_lib import send_success_response, send_error_response
from ..services import getter as getter_service
from ...common import exceptions as ex
from ...common.error_manager import ErrorManager
from ...common import rt_storage




TOOL = 'forecasting'

def index_view(req):
    # service.recreate_db(req)
    # service.fillin_db(req)
    # getter_service.set_permissions_template(req)
    # getter_service.init_user_wb(req, 1, 1)
    # getter_service.update_user_perms(req)
    # u_perms = getter_service.get_permissions(req, 1, 1)

    # getter_service.tmp_workbench(req)

    return render_to_response('iap.forecasting:templates/index.jinja2',
                              {'title': 'Forecast index'},
                              request=req)


def get_index_page_data(req):
    # 1.Get all available dimensions
    # 2.Get types for of widget for each of them
    # 3.Get available content for every dimension (depends
    # on current|default selection) with selection
    # 4.Get available content blocks
    # 5.Get type of each block
    # 6.Get data for content blocks (depends on values in bullet no.3)

    # data = {
    #     'nav_panel': {
    #         'order': ['product_dimension', 'region_dimension', 'timeseria_dimension'],
    #         'dimensions': [
    #             {
    #                 'name': 'product_dimension',
    #                 'widget': 'hierarchy',
    #                 'data': getter_service.get_hierarchy()
    #             },
    #             {
    #                 'name': 'region_dimension',
    #                 'widget': 'hierarchy',
    #                 'data': getter_service.get_hierarchy1()
    #             },
    #             {
    #                 'name': 'timeseria_dimension',
    #                 'widget': 'dropdown',
    #                 'data': getter_service.get_dropdown()
    #             }
    #         ]
    #     },
    #     'content': {
    #         'order': ['drivers_grid'],
    #         'zones': [
    #             {
    #                 'name': 'drivers_grid',
    #                 'widget': 'timeseries',
    #                 'data': getter_service.get_time_series()
    #             }
    #         ]
    #     }
    # }
    data = getter_service.tmp_workbench(req)

    return send_success_response(data)


def get_ui_config(req):
    ui_conf = {
        'widgets': {
            'hierarhy': {
                'default': {

                },
                'geography': {

                },
                'product': {

                }
            }
        },
        'not_widgets': {

        }
    }
    return send_success_response(ui_conf)


def get_scenarios_list(req):
    scenarios = [
        {
            'id': 1,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 2,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': True,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 3,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 4,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        },
        {
            'id': 5,
            'name': 'Default',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 6,
            'name': 'Argentina finalized 1.0',
            'author': 'Arthur Pirozhkov',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': True
            }
        },
        {
            'id': 7,
            'name': 'Brazil finalized 1.0',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': True,
            },
            'permissions': {
                'view': True,
                'edit': True,
                'delete': False
            }
        },
        {
            'id': 8,
            'name': 'Brazil finalized 1.1',
            'author': 'John Smith',
            'status': {
                'selected': False,
                'disabled': False,
            },
            'permissions': {
                'view': True,
                'edit': False,
                'delete': False
            }
        }
    ]
    return send_success_response(scenarios)


def get_dashboard_data(req):
    # Get parameters from request.
    try:
        user_id = req.user
        entity_id = req.json_body['entity_id']
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt_storage.get_wb(user_id, TOOL)
        data = getter_service.get_entity_data(wb.container, entity_id)
        return send_success_response(data)
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)


def get_dashboard_data_for_period(req):
    try:
        user_id = req.get_user()
        entity_id = req.json_body['entity_id']
        period = (req.json_body['period'][0], req.json_body['period'][1])
    except KeyError:
        msg = ErrorManager.get_error_message(ex.InvalidRequestParametersError)
        return send_error_response(msg)
    try:
        wb = rt_storage.get_wb(user_id, TOOL)
        dec = getter_service.get_decomposition(wb.container, entity_id, period)
        cagrs = getter_service.get_cagrs(wb.container, entity_id, period)
        return send_success_response(dict(dec=dec, cagrs=cagrs))
    except Exception as e:
        msg = ErrorManager.get_error_message(e)
        return send_error_response(msg)

