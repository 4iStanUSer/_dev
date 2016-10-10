dev_template = {
    'tool_id': 1,
    'configuration': [
        {
            'name': 'available_dimensions',
            'value': [
                'geography', 'category', 'time'
            ]
        },
        {
            'name': 'dimension_geography_widget',
            'value': 'hierarchy'
        },
        {
            'name': 'dimension_category_widget',
            'value': 'hierarchy'
        },
        {
            'name': 'dimension_time_widget',
            'value': 'dropdown'
        },
        {
            'name': 'cell_bg',
            'value': '#ccc'
        }],
    'top_entity': {'path': ['US']},
    'timelines': {
        'names': ['annual', '4-4-5'],
        'alias': {'history': {'annual': ('2011', '2015'), '4-4-5': ('Jan-11', 'Dec-15')},
                  'forecast': {'annual': ('2016', '2017'), '4-4-5': ('Jan-16', 'Dec-17')}},
        'top_ts_points': [
            {
                'name_full': '2011',
                'name_short': '2011',
                'children': [
                    {'name_full': 'Jan-11', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-11', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-11', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-11', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-11', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-11', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-11', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-11', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-11', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-11', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-11', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-11', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2012',
                'name_short': '2012',
                'children': [
                    {'name_full': 'Jan-12', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-12', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-12', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-12', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-12', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-12', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-12', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-12', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-12', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-12', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-12', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-12', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2013',
                'name_short': '2013',
                'children': [
                    {'name_full': 'Jan-13', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-13', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-13', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-13', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-13', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-13', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-13', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-13', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-13', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-13', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-13', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-13', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2014',
                'name_short': '2014',
                'children': [
                    {'name_full': 'Jan-14', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-14', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-14', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-14', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-14', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-14', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-14', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-14', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-14', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-14', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-14', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-14', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2015',
                'name_short': '2015',
                'children': [
                    {'name_full': 'Jan-15', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-15', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-15', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-15', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-15', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-15', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-15', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-15', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-15', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-15', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-15', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-15', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2016',
                'name_short': '2016',
                'children': [
                    {'name_full': 'Jan-16', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-16', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-16', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-16', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-16', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-16', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-16', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-16', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-16', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-16', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-16', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-16', 'name_short': 'Dec', 'children': []}
                ]
            },
            {
                'name_full': '2017',
                'name_short': '2017',
                'children': [
                    {'name_full': 'Jan-17', 'name_short': 'Jan', 'children': []},
                    {'name_full': 'Feb-17', 'name_short': 'Feb', 'children': []},
                    {'name_full': 'Mar-17', 'name_short': 'Mar', 'children': []},
                    {'name_full': 'Apr-17', 'name_short': 'Apr', 'children': []},
                    {'name_full': 'May-17', 'name_short': 'May', 'children': []},
                    {'name_full': 'Jun-17', 'name_short': 'Jum', 'children': []},
                    {'name_full': 'Jul-17', 'name_short': 'Jul', 'children': []},
                    {'name_full': 'Aug-17', 'name_short': 'Aug', 'children': []},
                    {'name_full': 'Sep-17', 'name_short': 'Sep', 'children': []},
                    {'name_full': 'Oct-17', 'name_short': 'Oct', 'children': []},
                    {'name_full': 'Nov-17', 'name_short': 'Nov', 'children': []},
                    {'name_full': 'Dec-17', 'name_short': 'Dec', 'children': []}
                ]
            }
        ]
    },
    'structure': [
        {
            'meta': ('Geography', 'Country'),
            'variables': {},
            'coefficients': {}
        },
        {
            'meta': ('Products', 'Brand'),
            'variables': {
                    'Media Spend - TV': ['4-4-5', 'annual'],
                    'Media Spend - Digital': ['4-4-5', 'annual'],
                    'Media Spend - Partnership': ['4-4-5', 'annual'],
                    'Media Spend - Print': ['4-4-5', 'annual'],
                    'Value': ['4-4-5', 'annual'],
                    'Units': ['4-4-5', 'annual'],
                    'Average Retail Price': ['4-4-5', 'annual']
                },
            'coefficients': {}
        },
        {
            'meta': ('Products', 'Segment'),
            'variables': {
                    'Value': ['4-4-5', 'annual'],
                    'Units': ['4-4-5', 'annual'],
                    'TDP': ['4-4-5'],
                    'Base Value': ['4-4-5'],
                    'Base Units': ['4-4-5'],
                    'TPR Dollars': ['4-4-5'],
                    'TPR Base Dollars': ['4-4-5'],
                    'TPR Units': ['4-4-5'],
                    'TPR Base Units': ['4-4-5'],
                    'QM Dollars': ['4-4-5'],
                    'QM Base Dollars': ['4-4-5'],
                    'QM Units': ['4-4-5'],
                    'QM Base Units': ['4-4-5'],
                    'Average Retail Price': ['4-4-5', 'annual'],
                    'Base Price': ['4-4-5'],
                    'TPR % Promo Support': ['4-4-5'],
                    'TPR % Discount': ['4-4-5'],
                    'TPR Base Price Index': ['4-4-5'],
                    'QM % Promo Support': ['4-4-5'],
                    'QM % Discount': ['4-4-5'],
                    'QM Base Price Index': ['4-4-5'],
                    'Quality Merch Lift': ['4-4-5'],
                    'Baseline units': ['4-4-5'],
                    'Promo Price Elasticity': ['4-4-5'],
                },
            'coefficients': {
                'TDP Incrementality': ['4-4-5'],
                'Everyday Price Elasticity': ['4-4-5'],
                'Advertising - TV sensitivity': ['4-4-5'],
                'Advertising - Digital sensitivity': ['4-4-5'],
                'Advertising - Partnership sensitivity': ['4-4-5'],
                'Advertising - Print sensitivity': ['4-4-5'],
                'Accumulation - TV': ['4-4-5'],
                'Accumulation - Digital': ['4-4-5'],
                'Accumulation - Partnership': ['4-4-5'],
                'Accumulation - Print': ['4-4-5'],
                'Lag - TV': ['4-4-5'],
                'Lag - Digital': ['4-4-5'],
                'Lag - Partnership': ['4-4-5'],
                'Lag - Print': ['4-4-5'],
                'Coverage Factor': ['4-4-5']
            }
        },
        {
            'meta': ('Chanel Distribution', 'Chanel'),
            'variables': {
                'Value': ['4-4-5', 'annual'],
                'Units': ['4-4-5', 'annual'],
                'TDP': ['4-4-5', 'annual'],
                'Base Value': ['4-4-5'],
                'Base Units': ['4-4-5'],
                'TPR Dollars': ['4-4-5'],
                'TPR Base Dollars': ['4-4-5'],
                'TPR Units': ['4-4-5'],
                'TPR Base Units': ['4-4-5'],
                'QM Dollars': ['4-4-5'],
                'QM Base Dollars': ['4-4-5'],
                'QM Units': ['4-4-5'],
                'QM Base Units': ['4-4-5'],
                'Display': ['4-4-5'],
                'Display parameters': ['4-4-5'],
                'Promo': ['4-4-5'],
                'Promo parameters': ['4-4-5'],
                'Baseline units': ['4-4-5']
            },
            'coefficients': {
                'PPE': ['4-4-5'],
                'QM Lift': ['4-4-5'],
                'Promotion Discount': ['4-4-5'],
                'Promotion Support': ['4-4-5']
            }
        }
    ],
    'exchange_rules': [
        {
            'meta': ('Products', 'Brand'),
            'input_variables': [
                {
                    'cont_var': 'Media Spend - TV',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TV',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Digital',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Digital',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Partnership',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Partnership',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Print',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Print',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Value',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Value',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Average Retail Price',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Average Retail Price',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                }
            ],
            'output_variables': []
        },
        {
            'meta': ('Products', 'Segment'),
            'input_variables': [
                {
                    'cont_var': 'Value',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Value',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TDP',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TDP',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Base Value',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Base Value',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Base Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Base Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Base Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Base Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                }
            ],
            'output_variables': []
        },
        {
            'meta': ('Chanel Distribution', 'Chanel'),
            'input_variables': [
                {
                    'cont_var': 'Value',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Value',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TDP',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TDP',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Base Value',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Base Value',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Base Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Base Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'TPR Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'TPR Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Base Dollars',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Base Dollars',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'QM Base Units',
                    'cont_ts': '4-4-5',
                    'wh_var': 'QM Base Units',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Display',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Display',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Display parameters',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Display parameters',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Promo',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Promo',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Promo parameters',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Promo parameters',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                }
            ],
            'output_variables': []
        }
    ],
    'dev_storage': [
        {
            'path': ['US', 'BAND-AID', 'DECORATED BNDG'],
            'coefficients': {
                'TDP Incrementality':  0.40 ,
                'Everyday Price Elasticity':  -0.45,
                'Advertising - TV sensitivity': 0.02,
                'Advertising - Digital sensitivity': 0.32,
                'Advertising - Partnership sensitivity': 0.09,
                'Advertising - Print sensitivity': 0.15,
                'Accumulation - TV': 2,
                'Accumulation - Digital': 1,
                'Accumulation - Partnership': 1,
                'Accumulation - Print': 6,
                'Lag - TV': 0,
                'Lag - Digital': 0,
                'Lag - Partnership': 0,
                'Lag - Print': 1
            }
        },
        {
            'path': ['US', 'BAND-AID', 'PREMIUM BNDG'],
            'coefficients':{
                'TDP Incrementality': 0.4,
                'Everyday Price Elasticity': -0.25,
                'Advertising - TV sensitivity': 0.03,
                'Advertising - Digital sensitivity': 0,
                'Advertising - Partnership sensitivity': 0.01,
                'Advertising - Print sensitivity': 0.1,
                'Accumulation - TV': 5,
                'Accumulation - Digital': 0,
                'Accumulation - Partnership': 4,
                'Accumulation - Print': 6,
                'Lag - TV': 0,
                'Lag - Digital': 0,
                'Lag - Partnership': 0,
                'Lag - Print': 1
            }
        },
        {
            'path': ['US', 'BAND-AID', 'VALUE BNDG'],
            'coefficients': {
                'TDP Incrementality': 0.4,
                'Everyday Price Elasticity': -0.3,
                'Advertising - TV sensitivity': 0.03,
                'Advertising - Digital sensitivity': 0.07,
                'Advertising - Partnership sensitivity': 0,
                'Advertising - Print sensitivity': 0.08,
                'Accumulation - TV': 5,
                'Accumulation - Digital': 1,
                'Accumulation - Partnership': 0,
                'Accumulation - Print': 4,
                'Lag - TV': 0,
                'Lag - Digital': 0,
                'Lag - Partnership': 0,
                'Lag - Print': 1
            }
        },
        {
            'path': ['US', 'BAND-AID', 'DECORATED BNDG', 'Walmart Total US TA'],
            'coefficients': {
                'PPE': {'New @ $XX': -1.10, 'Buy @ $XX': -1.10, 'ADS': -1.10},
                'QM Lift': {'New @ $XX': 1.15, 'Buy @ $XX': 1.06, 'ADS': 1.20},
                'Promotion Discount': {'New @ $XX': 0, 'Buy @ $XX': 0, 'ADS': 0},
                'Promotion Support': {'New @ $XX': 0.42, 'Buy @ $XX': 0.41,'ADS': 0.41}
            }
        },
        {
            'path': ['US', 'BAND-AID', 'PREMIUM BNDG', 'Walmart Total US TA'],
            'coefficients': {
                'PPE': {'Buy @ $XX': -1.3, 'ADS': -1.3},
                'QM Lift': {'Buy @ $XX': 1.19, 'ADS': 1.4},
                'Promotion Discount': {'Buy @ $XX': 0.01, 'ADS': 0.01},
                'Promotion Support': {'Buy @ $XX': 0.1,'ADS': 0.1}
            }
        },
        {
            'path': ['US', 'BAND-AID', 'VALUE BNDG', 'Walmart Total US TA'],
            'coefficients': {
                'PPE': {'ADS': -1.3},
                'QM Lift': {'ADS': 1.4},
                'Promotion Discount': {'ADS': 0.01},
                'Promotion Support': {'ADS': 0.1}
            }
        }
    ]
}