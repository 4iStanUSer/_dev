from ..common.helper_lib import send_success_response, send_error_response


def temp_routing(config):
    config.add_route('temp.check_logged_in',
                     '/check_logged_in')
    config.add_view(check_logged_in,
                    route_name='temp.check_logged_in',
                    request_method='POST', renderer='json')

    config.add_route('temp.login',
                     '/login')
    config.add_view(login,
                    route_name='temp.login',
                    request_method='POST', renderer='json')

    config.add_route('temp.logout',
                     '/logout')
    config.add_view(logout,
                    route_name='temp.logout',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_urls',
                     '/get_urls')
    config.add_view(get_urls,
                    route_name='temp.get_urls',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_page_static_data',
                     '/get_page_static_data')
    config.add_view(get_page_static_data,
                    route_name='temp.get_page_static_data',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_languages',
                     '/get_languages')
    config.add_view(get_languages,
                    route_name='temp.get_languages',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_top_menu',
                     '/get_top_menu')
    config.add_view(get_top_menu,
                    route_name='temp.get_top_menu',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_dashboard_data',
                     '/get_dashboard_data')
    config.add_view(get_dashboard_data,
                    route_name='temp.get_dashboard_data',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_changes_for_period',
                     '/get_changes_for_period')
    config.add_view(get_changes_for_period,
                    route_name='temp.get_changes_for_period',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_decomposition_for_period',
                     '/get_decomposition_for_period')
    config.add_view(get_decomposition_for_period,
                    route_name='temp.get_decomposition_for_period',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_options_for_entity_selector',
                     '/get_options_for_entity_selector')
    config.add_view(get_options_for_entity_selector,
                    route_name='temp.get_options_for_entity_selector',
                    request_method='POST', renderer='json')

    config.add_route('temp.get_entity_selectors_config',
                     '/get_entity_selectors_config')
    config.add_view(get_entity_selectors_config,
                    route_name='temp.get_entity_selectors_config',
                    request_method='POST', renderer='json')


def get_urls(req):
    data = {
        'check_logged_in': {
            'url': '/temp/check_logged_in',
            'allowNotAuth': True,
        },
        'login': {
            'url': '/temp/login',
            'allowNotAuth': True,
        },
        'logout': {
            'url': '/temp/logout',
            'allowNotAuth': True,
        },
        'landing': {
            'url': '/landing',
            'allowNotAuth': True,
        },
        'set_tool_selection': {
            'url': '/set_tool_selection',
            'allowNotAuth': True,
        },
        'get_languages': {
            'url': '/temp/get_languages',
            'allowNotAuth': True,
        },
        'forecast/get_top_menu': {
            'url': '/temp/get_top_menu',
            'allowNotAuth': True,
        },

        'forecast/get_entity_selectors_config': {
            'url': '/temp/get_entity_selectors_config',
            'allowNotAuth': True,
        },
        'forecast/get_options_for_entity_selector': {
            'url': '/temp/get_options_for_entity_selector',
            'allowNotAuth': True,
        },

        'forecast/get_dashboard_data': {
            'url': '/temp/get_dashboard_data',
            'allowNotAuth': True,
        },
        'forecast/get_changes_for_period': {
            'url': '/temp/get_changes_for_period',
            'allowNotAuth': True,
        },
        'forecast/get_decomposition_for_period': {
            'url': '/temp/get_decomposition_for_period',
            'allowNotAuth': True,
        },

        'forecast/get_page_static_data': {
            'url': '/temp/get_page_static_data',
            'allowNotAuth': True,
        },
        'forecast/get_scenarios_list': {
            'url': '/forecast/get_scenarios_list',
            'allowNotAuth': True,
        }
    }
    return send_success_response(data)

# ----TEMP CODE
class Auth:  # TEMP Class
    is_logged_in = False


def send_auth_error():
    data = 'auth-error'
    return send_error_response(data)

auth = Auth()
# ----.TEMP CODE


def check_logged_in(req):
    return send_success_response(auth.is_logged_in)


def login(req):
    auth.is_logged_in = True
    # Return UserModel
    data = {
        'logged': True,
        'user': {
            'email': 'test@test.test',
            'name': 'Main Tester'
        }
    }
    return send_success_response(data)


def logout(req):
    auth.is_logged_in = False
    data = {}
    return send_success_response(data)


def get_page_static_data(req):
    if auth.is_logged_in:
        data = {
            'state': {
                'forecast_timescale': 'annual', # annual | quarterly | monthly
                'forecast_absolute_rate': 'absolute', # absolute | rate
                'forecast_collapse_expand': 'collapse', # collapse | expand
                'forecast_active_tab': 'all', # all | (name of variable)
                'forecast_tab': 'all', # all | ( or name of variable)
                'decomp_value_volume_price': 'value', # value | volume | price(name of type)
                'd_summary_table_collapsed_expanded': 'expanded', # collapsed | expanded
                'd_details_table_collapsed_expanded': 'expanded', # collapsed | expanded
                'd_details_selected_factor': None, # null(get first) | factor (variable) id
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
    else:
        return send_auth_error()


def get_languages(req):
    if auth.is_logged_in:
        data = [
            {
                'id': 'en',
                'name': 'English',
                'selected': True
            },
            {
                'id': 'ru',
                'name': 'Russian',
                'selected': False
            },
            {
                'id': 'sp',
                'name': 'Spain',
                'selected': False
            }
        ]
        return send_success_response(data)
    else:
        return send_auth_error()


def get_top_menu(req):
    if auth.is_logged_in:
        data = [
            {
                'key': 'home',
                'name': 'Home',
                'disabled': False
            },
            {
                'key': 'dashboard',
                'name': 'Dashboard',
                'disabled': False
            },
            {
                'key': 'comparison',
                'name': 'Comparison',
                'disabled': True
            },
            {
                'key': 'scenarios',
                'name': 'Scenarios',
                'disabled': False
            },
            {
                'key': 'simulator',
                'name': 'Simulator',
                'disabled': False
            }
        ]
        return send_success_response(data)
    else:
        return send_auth_error()


def get_dashboard_data(req):
    if auth.is_logged_in:
        data = {
            "config": {
                "decomp_timescales": [
                    "annual"
                ],
                "main_period": {
                    "timescale": "annual",
                    "mid": "2015",
                    "end": "2018",
                    "start": "2013"
                },
                "decomp_period": {
                    "timescale": "annual",
                    "end": "2018",
                    "start": "2014"
                }
            },
            "data": {
                "insights": [
                    {
                        "text": "insight1"
                    },
                    {
                        "text": "insight2"
                    }
                ],
                "variables": [
                    {
                        "id": "Avg % Discount",
                        "full_name": "Avg % Discount",
                        "short_name": "Avg % Discount",
                        "type": "driver",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Above Unit Price",
                        "full_name": "Above Unit Price",
                        "short_name": "Above Unit Price",
                        "type": "driver",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Price per Unit",
                        "full_name": "Price per Unit",
                        "short_name": "Price per Unit",
                        "type": "driver",
                        "metric": "Dollar Per Unit",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Value",
                        "full_name": "Value",
                        "short_name": "Value",
                        "type": "output",
                        "metric": "Dollar",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Avg % Volume sold as Promo",
                        "full_name": "Avg % Volume sold as Promo",
                        "short_name": "Avg % Volume sold as Promo",
                        "type": "driver",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Distribution",
                        "full_name": "Distribution",
                        "short_name": "Distribution",
                        "type": "driver",
                        "metric": "TDP",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Media Spend",
                        "full_name": "Media Spend",
                        "short_name": "Media Spend",
                        "type": "driver",
                        "metric": "Dollar",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Unit Volume",
                        "full_name": "Unit Volume",
                        "short_name": "Unit Volume",
                        "type": "driver",
                        "metric": "Unit",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "EQ Volume",
                        "full_name": "EQ Volume",
                        "short_name": "EQ Volume",
                        "type": "output",
                        "metric": "Liter",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Premiumization",
                        "full_name": "Premiumization",
                        "short_name": "Premiumization",
                        "type": "driver",
                        "metric": "index",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Avg % Promo Support",
                        "full_name": "Avg % Promo Support",
                        "short_name": "Avg % Promo Support",
                        "type": "driver",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Unit Size",
                        "full_name": "Unit Size",
                        "short_name": "Unit Size",
                        "type": "driver",
                        "metric": "Litter per Unit",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Innovation TDP share",
                        "full_name": "Innovation TDP share",
                        "short_name": "Innovation TDP share",
                        "type": "driver",
                        "metric": "% of TDP",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "Price per EQ",
                        "full_name": "Price per EQ",
                        "short_name": "Price per EQ",
                        "type": "output",
                        "metric": "Dollar Per Liter",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "LTT",
                        "full_name": "LTT",
                        "short_name": "LTT",
                        "type": "driver",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "ImpactVar1",
                        "full_name": "ImpactVar1",
                        "short_name": "ImpactVar1",
                        "type": "impact",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "ImpactVar2",
                        "full_name": "ImpactVar2",
                        "short_name": "ImpactVar2",
                        "type": "impact",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "ImpactVar3",
                        "full_name": "ImpactVar3",
                        "short_name": "ImpactVar3",
                        "type": "impact",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "ImpactVar4",
                        "full_name": "ImpactVar4",
                        "short_name": "ImpactVar4",
                        "type": "impact",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    },
                    {
                        "id": "ImpactVar5",
                        "full_name": "ImpactVar5",
                        "short_name": "ImpactVar5",
                        "type": "impact",
                        "metric": "%",
                        "format": "",
                        "hint": ""
                    }
                ],
                "variable_values": {
                    "annual": {
                        "Avg % Discount": {
                            "2013": 0.15672912,
                            "2014": 0.124825838,
                            "2015": 0.021315367,
                            "2016": 0.073070602,
                            "2017": 0.073070602,
                            "2018": 0.073070602
                        },
                        "Above Unit Price": {
                            "2013": 0,
                            "2014": 0,
                            "2015": 0,
                            "2016": -0.023345156,
                            "2017": -0.023345156,
                            "2018": -0.023345156
                        },
                        "Price per Unit": {
                            "2013": 3.134247748,
                            "2014": 3.070108835,
                            "2015": 2.976280282,
                            "2016": 2.863626067,
                            "2017": 2.818788424,
                            "2018": 2.768048625
                        },
                        "Value": {
                            "2013": 237288.8064,
                            "2014": 245366.2606,
                            "2015": 241606.5798,
                            "2016": 243489.0721562347,
                            "2017": 250075.20994703867,
                            "2018": 255400.3457041838
                        },
                        "Avg % Volume sold as Promo": {
                            "2013": 0.142749047,
                            "2014": 0.156890702,
                            "2015": 0.192484476,
                            "2016": 0,
                            "2017": 0,
                            "2018": 0
                        },
                        "Distribution": {
                            "2013": 2817.679167,
                            "2014": 2812.516667,
                            "2015": 2959.427069,
                            "2016": 3030.30102,
                            "2017": 3101.174971,
                            "2018": 3172.048922
                        },
                        "Media Spend": {
                            "2013": 48195.8222,
                            "2014": 47651.25748,
                            "2015": 45410.61262,
                            "2016": 44897.51799,
                            "2017": 44390.22082,
                            "2018": 43888.6556
                        },
                        "Unit Volume": {
                            "2013": 75.7083758,
                            "2014": 79.9210301,
                            "2015": 81.17736128,
                            "2016": 85028.2356911632,
                            "2017": 88717.26867395375,
                            "2018": 92267.2901760112
                        },
                        "EQ Volume": {
                            "2013": 28293.6806,
                            "2014": 30136.8716,
                            "2015": 31455.34679,
                            "2016": 33233.539474089965,
                            "2017": 34973.83882599352,
                            "2018": 36683.688556046116
                        },
                        "Premiumization": {
                            "2013": 1,
                            "2014": 0.994448796,
                            "2015": 0.983935894,
                            "2016": 0.975903841,
                            "2017": 0.967871788,
                            "2018": 0.959839735
                        },
                        "Avg % Promo Support": {
                            "2013": 0.067045178,
                            "2014": 0.076185237,
                            "2015": 0.125144696,
                            "2016": 0.100664966,
                            "2017": 0.100664966,
                            "2018": 0.100664966
                        },
                        "Unit Size": {
                            "2013": 0.373719292,
                            "2014": 0.377083123,
                            "2015": 0.387489151,
                            "2016": 0.390852982,
                            "2017": 0.394216812,
                            "2018": 0.397580643
                        },
                        "Innovation TDP share": {
                            "2013": 0.041534083,
                            "2014": 0.025890229,
                            "2015": 0.051369726,
                            "2016": 0.056287547,
                            "2017": 0.061205369,
                            "2018": 0.066123191
                        },
                        "Price per EQ": {
                            "2013": 8.386636215,
                            "2014": 8.141729635,
                            "2015": 7.680938359,
                            "2016": 7.32660667534577,
                            "2017": 7.150350614676474,
                            "2018": 6.962231873547224
                        },
                        "LTT": {
                            "2013": 0,
                            "2014": 0,
                            "2015": 0,
                            "2016": 0.0104958,
                            "2017": 0.0104958,
                            "2018": 0.0104958
                        },
                        "ImpactVar1": {
                            "2013": 0.351974,
                            "2014": 0.997305,
                            "2015": 0.718144,
                            "2016": 0.636752,
                            "2017": 0.769829,
                            "2018": 0.664442
                        },
                        "ImpactVar2": {
                            "2013": 0.074939,
                            "2014": 0.223951,
                            "2015": 0.400238,
                            "2016": 0.729591,
                            "2017": 0.527484,
                            "2018": 0.981372
                        },
                        "ImpactVar3": {
                            "2013": 0.503847,
                            "2014": 0.100241,
                            "2015": 0.404303,
                            "2016": 0.753095,
                            "2017": 0.471066,
                            "2018": 0.743271
                        },
                        "ImpactVar4": {
                            "2013": 0.211345,
                            "2014": 0.221179,
                            "2015": 0.164605,
                            "2016": 0.454385,
                            "2017": 0.768253,
                            "2018": 0.999185
                        },
                        "ImpactVar5": {
                            "2013": 0.742955,
                            "2014": 0.504349,
                            "2015": 0.887565,
                            "2016": 0.526211,
                            "2017": 0.696226,
                            "2018": 0.656456
                        }
                    }
                },
                "timescales": [
                    {
                        "id": "annual",
                        "full_name": "annual",
                        "short_name": "annual",
                        "lag": 1
                    }
                ],
                "timelables": [
                    {
                        "id": "2013",
                        "full_name": "2013",
                        "short_name": "2013",
                        "parent_index": None,
                        "timescale": "annual"
                    },
                    {
                        "id": "2014",
                        "full_name": "2014",
                        "short_name": "2014",
                        "parent_index": None,
                        "timescale": "annual"
                    },
                    {
                        "id": "2015",
                        "full_name": "2015",
                        "short_name": "2015",
                        "parent_index": None,
                        "timescale": "annual"
                    },
                    {
                        "id": "2016",
                        "full_name": "2016",
                        "short_name": "2016",
                        "parent_index": None,
                        "timescale": "annual"
                    },
                    {
                        "id": "2017",
                        "full_name": "2017",
                        "short_name": "2017",
                        "parent_index": None,
                        "timescale": "annual"
                    },
                    {
                        "id": "2018",
                        "full_name": "2018",
                        "short_name": "2018",
                        "parent_index": None,
                        "timescale": "annual"
                    }
                ],
                "decomp_types": [
                    {
                        "id": "value",
                        "full_name": "Value",
                        "short_name": "value"
                    },
                    {
                        "id": "volume",
                        "full_name": "Volume",
                        "short_name": "volume"
                    }
                ],
                "change_over_period": {
                    "annual": {
                        "Avg % Discount": [
                            {
                                "abs": -0.045903282,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            },
                            {
                                "abs": -0.039903282,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": -0.03190328200000003,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": -0.10351047099999999,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.0517552349999999,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Above Unit Price": [
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Price per Unit": [
                            {
                                "abs": -0.020463893781507148,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": -0.03056196312336934,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": -0.037850674105295745,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": -0.015657645918474627,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": -0.018000570233645874,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "abs": [
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Avg % Volume sold as Promo": [
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Distribution": [
                            {
                                "abs": -0.0018321816268018765,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.05223450005603114,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.023948537790440927,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.02338841934587732,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.022853902686163607,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Media Spend": [
                            {
                                "abs": -0.011299002592801588,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": -0.047021736224703736,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": -0.011299002598657237,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": -0.011299002544260639,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": -0.011299002589643004,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Unit Volume": [
                            {
                                "abs": 0.055643173631523046,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.015719656996763476,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 1046.4377874624504,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.0433859758797035,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.04001499995569291,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "EQ Volume": [
                            {
                                "abs": 0.06514497092329519,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.0437495705426838,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.05653069718040027,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.05236575397755483,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.04888939239869172,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Premiumization": [
                            {
                                "abs": -0.005551203999999976,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": -0.010571587036241947,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": -0.008163187306184372,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": -0.00823037338573207,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": -0.008298674576099896,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Avg % Promo Support": [
                            {
                                "abs": 0.009140058999999923,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.04895945899999998,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": -0.024479730000000033,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Unit Size": [
                            {
                                "abs": 0.009000956257832149,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.027596111746427843,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.008681097241868496,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.008606381823639264,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.008532946585748213,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Innovation TDP share": [
                            {
                                "abs": -0.015643854000000013,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.025479497000000073,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.004917821000000044,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.004917821999999905,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.004917821999999905,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "Price per EQ": [
                            {
                                "abs": -0.029202003487640127,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": -0.0565962389636635,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": -0.046131301553676396,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": -0.02405698415098534,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": -0.02630902332860796,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "LTT": [
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.010495799999999944,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "ImpactVar1": [
                            {
                                "abs": 0.0456,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.0498,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.0347,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.0235,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.3658,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0.0497,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0.0936,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ],
                        "ImpactVar2": [
                            {
                                "abs": 0.0569,
                                "rate": 0,
                                "end": "2014",
                                "start": "2013"
                            },
                            {
                                "abs": 0.0698,
                                "rate": 0,
                                "end": "2015",
                                "start": "2014"
                            },
                            {
                                "abs": 0.0703,
                                "rate": 0,
                                "end": "2016",
                                "start": "2015"
                            },
                            {
                                "abs": 0.0654,
                                "rate": 0,
                                "end": "2017",
                                "start": "2016"
                            },
                            {
                                "abs": 0.0692,
                                "rate": 0,
                                "end": "2018",
                                "start": "2017"
                            },
                            {
                                "abs": 0.0656,
                                "rate": 0,
                                "end": "2015",
                                "start": "2013"
                            },
                            {
                                "abs": 0.0512,
                                "rate": 0,
                                "end": "2018",
                                "start": "2015"
                            }
                        ]
                    }
                },
                "decomp": {
                    "annual": {
                        "value": [
                            {
                                "start": "2014",
                                "end": "2018",
                                "factors": [
                                    {
                                        "var_id": "ImpactVar1",
                                        "abs": 0.21990784,
                                        "rate": 0.0359802
                                    },
                                    {
                                        "var_id": "ImpactVar2",
                                        "abs": 0.21163726,
                                        "rate": 0.0510542
                                    },
                                    {
                                        "var_id": "ImpactVar3",
                                        "abs": 0.21794359,
                                        "rate": 0.0206714
                                    },
                                    {
                                        "var_id": "ImpactVar4",
                                        "abs": 0.21754937,
                                        "rate": 0.0754937
                                    },
                                    {
                                        "var_id": "ImpactVar5",
                                        "abs": 0.21127042,
                                        "rate": 0.038778
                                    }
                                ]
                            },
                        #     {
                        #         "start": "2015",
                        #         "end": "2018",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.21990784,
                        #                 "rate": 0.0359802
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.21163726,
                        #                 "rate": 0.0510542
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.21794359,
                        #                 "rate": 0.0206714
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.21754937,
                        #                 "rate": 0.0754937
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.21127042,
                        #                 "rate": 0.038778
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2013",
                        #         "end": "2015",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.1990784,
                        #                 "rate": 0.0359802
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.1163726,
                        #                 "rate": 0.0510542
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.1794359,
                        #                 "rate": 0.0206714
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.1754937,
                        #                 "rate": 0.0754937
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.1127042,
                        #                 "rate": 0.038778
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2013",
                        #         "end": "2014",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.990784,
                        #                 "rate": 0.0359802
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.163726,
                        #                 "rate": 0.0510542
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.794359,
                        #                 "rate": 0.0206714
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.754937,
                        #                 "rate": 0.0754937
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.127042,
                        #                 "rate": 0.038778
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2014",
                        #         "end": "2015",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.978912,
                        #                 "rate": 0.0483124
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.23216,
                        #                 "rate": 0.0682931
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.610557,
                        #                 "rate": 0.0906985
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.475029,
                        #                 "rate": 0.0197856
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.207832,
                        #                 "rate": 0.0105532
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2015",
                        #         "end": "2016",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.240613,
                        #                 "rate": 0.0210588
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.598098,
                        #                 "rate": 0.0151758
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.692215,
                        #                 "rate": 0.0477526
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.234345,
                        #                 "rate": 0.085709
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.666541,
                        #                 "rate": 0.0668499
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2016",
                        #         "end": "2017",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.392542,
                        #                 "rate": 0.0953839
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.963472,
                        #                 "rate": 0.0226944
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.751981,
                        #                 "rate": 0.0800128
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.868217,
                        #                 "rate": 0.0102356
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.460591,
                        #                 "rate": 0.043915
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2017",
                        #         "end": "2018",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.624416,
                        #                 "rate": 0.0560729
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.871365,
                        #                 "rate": 0.0874228
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.444918,
                        #                 "rate": 0.0795486
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.392,
                        #                 "rate": 0.0489171
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.559849,
                        #                 "rate": 0.0232788
                        #             }
                        #         ]
                        #     }
                        ],
                        "volume": [
                            {
                                "start": "2014",
                                "end": "2018",
                                "factors": [
                                    {
                                        "var_id": "Premiumization",
                                        "abs": 2.45,
                                        "rate": 1
                                    },
                                    {
                                        "var_id": "ImpactVar1",
                                        "abs": 0.98542,
                                        "rate": 0.0738657
                                    },
                                    {
                                        "var_id": "ImpactVar2",
                                        "abs": 0.48134,
                                        "rate": 0.0652715
                                    },
                                    {
                                        "var_id": "ImpactVar3",
                                        "abs": 0.99519,
                                        "rate": 0.0976987
                                    },
                                    {
                                        "var_id": "ImpactVar4",
                                        "abs": 0.78942,
                                        "rate": 0.0626273
                                    },
                                    {
                                        "var_id": "ImpactVar5",
                                        "abs": 0.285773,
                                        "rate": 0.0355594
                                    }
                                ]
                            },
                        #     {
                        #         "start": "2013",
                        #         "end": "2014",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.98542,
                        #                 "rate": 0.0738657
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.48134,
                        #                 "rate": 0.0652715
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.99519,
                        #                 "rate": 0.0976987
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.78942,
                        #                 "rate": 0.0626273
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.285773,
                        #                 "rate": 0.0355594
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2014",
                        #         "end": "2015",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.528851,
                        #                 "rate": 0.0919143
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.763161,
                        #                 "rate": 0.0842327
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.537789,
                        #                 "rate": 0.0704983
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.923729,
                        #                 "rate": 0.0271423
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.68645,
                        #                 "rate": 0.0176666
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2015",
                        #         "end": "2016",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.524467,
                        #                 "rate": 0.0468196
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.611925,
                        #                 "rate": 0.093163
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.296334,
                        #                 "rate": 0.0101075
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.372081,
                        #                 "rate": 0.0741157
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.175675,
                        #                 "rate": 0.0812591
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2016",
                        #         "end": "2017",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.92559,
                        #                 "rate": 0.0343801
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.444639,
                        #                 "rate": 0.0254852
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.447989,
                        #                 "rate": 0.0689154
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.276602,
                        #                 "rate": 0.0293354
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.831093,
                        #                 "rate": 0.0587996
                        #             }
                        #         ]
                        #     },
                        #     {
                        #         "start": "2017",
                        #         "end": "2018",
                        #         "factors": [
                        #             {
                        #                 "var_id": "ImpactVar1",
                        #                 "abs": 0.235433,
                        #                 "rate": 0.011355
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar2",
                        #                 "abs": 0.14416,
                        #                 "rate": 0.084965
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar3",
                        #                 "abs": 0.444918,
                        #                 "rate": 0.0795486
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar4",
                        #                 "abs": 0.85634,
                        #                 "rate": 0.083107
                        #             },
                        #             {
                        #                 "var_id": "ImpactVar5",
                        #                 "abs": 0.789906,
                        #                 "rate": 0.0925784
                        #             }
                        #         ]
                        #     }
                        ]
                    }
                },
                "decomp_type_factors": {
                    "value": ["ImpactVar1", "ImpactVar2"],
                    "volume": ["ImpactVar2", "ImpactVar3"]
                },
                "factor_drivers": {
                    "ImpactVar1": [
                        {
                            "factor": "ImpactVar1",
                            "driver": "Avg % Discount"
                        }
                    ],
                    "ImpactVar2": [
                        {
                            "factor": "ImpactVar2",
                            "driver": "Above Unit Price"
                        }
                    ],
                    "ImpactVar3": [
                        {
                            "factor": "ImpactVar4",
                            "driver": "Price per Unit"
                        },
                        {
                            "factor": "ImpactVar5",
                            "driver": "Avg % Volume sold as Promo"
                        }
                    ]
                }
            }
        }
        return send_success_response(data)
    else:
        return send_auth_error()


def get_options_for_entity_selector(req):
    auth.is_logged_in = False
    if auth.is_logged_in:
        data = {
            'brand': {
                'data': [
                    {
                        'name': 'Puma',
                        'id': 'puma',
                        'parent_id': None
                    },
                    {
                        'name': 'Nike',
                        'id': 'nike',
                        'parent_id': None
                    },
                    {
                        'name': 'Adidas',
                        'id': 'adidas',
                        'parent_id': None
                    }
                ],
                'selected': ['puma', 'adidas']
            },
            'category': {
                'data': [
                    {
                        'name': 'Puma',
                        'id': 'puma',
                        'parent_id': None
                    },
                    {
                        'name': 'Nike',
                        'id': 'nike',
                        'parent_id': None
                    },
                    {
                        'name': 'Adidas',
                        'id': 'adidas',
                        'parent_id': None
                    },
                    {
                        'name': 'Puma Black',
                        'id': 'puma_black',
                        'parent_id': 'puma'
                    },
                    {
                        'name': 'Nike Black',
                        'id': 'nike_black',
                        'parent_id': 'nike'
                    },
                    {
                        'name': 'Adidas Black',
                        'id': 'adidas_black',
                        'parent_id': 'adidas'
                    },
                ],
                'selected': ['adidas']
            }
        }
        return send_success_response(data)
    else:
        return send_auth_error()


def get_entity_selectors_config(req):
    if auth.is_logged_in:
        data = {
            'selectors': {
                'brand': {
                    'name': 'Brand',
                    'placeholder': 'brand',
                    'multiple': True,  # false|true,
                    'type': 'flat',  # flat | hierarchical | region
                    'icon': '',
                    'disabled': False,
                },
                'category': {
                    'name': 'Category',
                    'placeholder': 'category',
                    'multiple': True,
                    'type': 'hierarchical', # flat | hierarchical | region
                    'icon': '',
                    'disabled': False,
                }
            },
            'order': ['brand', 'category']
        }
        return send_success_response(data)
    else:
        return send_auth_error()


def get_decomposition_for_period(req):
    if auth.is_logged_in:
        data = {
            "annual": {
                "value": [
                    {
                        "start": "2015",
                        "end": "2018",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.21990784,
                                "rate": 0.0359802
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.21163726,
                                "rate": 0.0510542
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.21794359,
                                "rate": 0.0206714
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.21754937,
                                "rate": 0.0754937
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.21127042,
                                "rate": 0.038778
                            }
                        ]
                    },
                    {
                        "start": "2013",
                        "end": "2015",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.1990784,
                                "rate": 0.0359802
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.1163726,
                                "rate": 0.0510542
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.1794359,
                                "rate": 0.0206714
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.1754937,
                                "rate": 0.0754937
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.1127042,
                                "rate": 0.038778
                            }
                        ]
                    },
                    {
                        "start": "2013",
                        "end": "2014",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.990784,
                                "rate": 0.0359802
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.163726,
                                "rate": 0.0510542
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.794359,
                                "rate": 0.0206714
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.754937,
                                "rate": 0.0754937
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.127042,
                                "rate": 0.038778
                            }
                        ]
                    },
                    {
                        "start": "2014",
                        "end": "2015",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.978912,
                                "rate": 0.0483124
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.23216,
                                "rate": 0.0682931
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.610557,
                                "rate": 0.0906985
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.475029,
                                "rate": 0.0197856
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.207832,
                                "rate": 0.0105532
                            }
                        ]
                    },
                    {
                        "start": "2015",
                        "end": "2016",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.240613,
                                "rate": 0.0210588
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.598098,
                                "rate": 0.0151758
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.692215,
                                "rate": 0.0477526
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.234345,
                                "rate": 0.085709
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.666541,
                                "rate": 0.0668499
                            }
                        ]
                    },
                    {
                        "start": "2016",
                        "end": "2017",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.392542,
                                "rate": 0.0953839
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.963472,
                                "rate": 0.0226944
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.751981,
                                "rate": 0.0800128
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.868217,
                                "rate": 0.0102356
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.460591,
                                "rate": 0.043915
                            }
                        ]
                    },
                    {
                        "start": "2017",
                        "end": "2018",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.624416,
                                "rate": 0.0560729
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.871365,
                                "rate": 0.0874228
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.444918,
                                "rate": 0.0795486
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.392,
                                "rate": 0.0489171
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.559849,
                                "rate": 0.0232788
                            }
                        ]
                    }
                ],
                "volume": [
                    {
                        "start": "2013",
                        "end": "2014",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.98542,
                                "rate": 0.0738657
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.48134,
                                "rate": 0.0652715
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.99519,
                                "rate": 0.0976987
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.78942,
                                "rate": 0.0626273
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.285773,
                                "rate": 0.0355594
                            }
                        ]
                    },
                    {
                        "start": "2014",
                        "end": "2015",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.528851,
                                "rate": 0.0919143
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.763161,
                                "rate": 0.0842327
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.537789,
                                "rate": 0.0704983
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.923729,
                                "rate": 0.0271423
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.68645,
                                "rate": 0.0176666
                            }
                        ]
                    },
                    {
                        "start": "2015",
                        "end": "2016",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.524467,
                                "rate": 0.0468196
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.611925,
                                "rate": 0.093163
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.296334,
                                "rate": 0.0101075
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.372081,
                                "rate": 0.0741157
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.175675,
                                "rate": 0.0812591
                            }
                        ]
                    },
                    {
                        "start": "2016",
                        "end": "2017",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.92559,
                                "rate": 0.0343801
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.444639,
                                "rate": 0.0254852
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.447989,
                                "rate": 0.0689154
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.276602,
                                "rate": 0.0293354
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.831093,
                                "rate": 0.0587996
                            }
                        ]
                    },
                    {
                        "start": "2017",
                        "end": "2018",
                        "factors": [
                            {
                                "var_id": "ImpactVar1",
                                "abs": 0.235433,
                                "rate": 0.011355
                            },
                            {
                                "var_id": "ImpactVar2",
                                "abs": 0.14416,
                                "rate": 0.084965
                            },
                            {
                                "var_id": "ImpactVar3",
                                "abs": 0.444918,
                                "rate": 0.0795486
                            },
                            {
                                "var_id": "ImpactVar4",
                                "abs": 0.85634,
                                "rate": 0.083107
                            },
                            {
                                "var_id": "ImpactVar5",
                                "abs": 0.789906,
                                "rate": 0.0925784
                            }
                        ]
                    }
                ]
            }
        }
        return send_success_response(data)
    else:
        return send_auth_error()


def get_changes_for_period(req):
    if auth.is_logged_in:
        data = {
            'get_changes_for_period': 1
        }
        return send_success_response(data)
    else:
        return send_auth_error()
