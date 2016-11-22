from ..common.helper_lib import send_success_response, send_error_response

def temp_routing(config):
    config.add_route('temp.get_page_static_data',
                     '/get_page_static_data')
    config.add_view(get_page_static_data,
                    route_name='temp.get_page_static_data',
                    request_method='POST', renderer='json')


def get_page_static_data(req):
    data = {
        'state': {
            'forecast_timescale': 'annual', # annual | quarterly | monthly
            'forecast_absolute_rate': 'absolute', # absolute | rate
            'forecast_collapse_expand': 'collapse', # collapse | expand
            'forecast_active_tab': 'all', # all | (name of variable)
            'forecast_tab': 'all', # all | ( or name of variable)
            'decomp_value_volume_price': 'Value', # value | volume | price(name of type)
            'd_summary_table_collapsed_expanded': 'expanded', # collapsed | expanded
            'd_details_table_collapsed_expanded': 'expanded', # collapsed | expanded
            'd_details_selected_megadriver': None, # null(get first) | mega driver key
        },
        'config': {
            'forecast_block': 'Forecast',
            'decomposition_block': 'Decomposition',
            'insights_block': 'Insights',
            'drivers_summary_block': 'Drivers Summary',

            'dashboard_tab': 'Dashboard',
            'drivers_summary_tab': 'Drivers Summary',
            'drivers_details_tab': 'Driver\'s Details',

            'value': 'Value',
            'growth_rate': 'Growth rate',
            'collapse': 'Collapse',
            'expand': 'Expand',
            'explore': 'Explore',
            'tab_all': 'All',
            'absolute': 'Absolute',
            'growth_cagr': 'Growth (CAGR)',

            'driver_contribution': 'Driver Contribution to Sales Growth,',
            'driver_change_cagr': 'Driver Change (CAGR)',

            'driver': 'Driver',
            'metric': 'Metric',
            'cagr': 'CAGR',

            'sub_drivers_dynamic': 'Sub-driver\'s dynamic',
            'sub_drivers_impact': 'Sub-driver\'s impact',
            'fact': 'Fact',

            'apply': 'Apply!',
            'cancel': 'Cancel!',
        }
    }
    return send_success_response(data)
