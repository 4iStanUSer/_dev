dev_template_JJLean = {
    'tool_id': 1,
    'configuration': [
        {
            'name': 'available_dimensions',
            'value': [
                'geography', 'category', 'channel'
            ]
        },
        {
            'name': 'dimension_geography_widget',
            'value': 'hierarchy'
        },
        {
            'name': 'dimension_category_widget',
            'value': 'hierarchy'
        }
    ],
    'top_entity': {},
    'entities': [
        ['US'],
        ['US', 'JJLean', 'BENADRYL'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI', 'Total'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI', 'Walmart'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI', 'Walgreens'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI', 'Target'],
        ['US', 'JJLean', 'BENADRYL', 'BENADRYL SI', 'CVS'],
        ['US', 'JJLean', 'BAND-AID'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED', 'Total'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED', 'Walmart'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED', 'Walgreens'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED', 'Target'],
        ['US', 'JJLean', 'BAND-AID', 'DECORATED', 'CVS'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE', 'Total'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE', 'Walmart'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE', 'Walgreens'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE', 'Target'],
        ['US', 'JJLean', 'BAND-AID', 'VALUE', 'CVS'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM', 'Total'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM', 'Walmart'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM', 'Walgreens'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM', 'Target'],
        ['US', 'JJLean', 'BAND-AID', 'PREMIUM', 'CVS']
    ],
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
            'path': ['US', 'BAND-AID', 'DECORATED'],
            'coefficients': [
                {'name': 'TDP Incrementality', 'ts': '4-4-5', 'value':  0.40},
                {'name': 'Everyday Price Elasticity', 'ts': '4-4-5', 'value':  -0.45},
                {'name': 'Advertising - TV sensitivity', 'ts': '4-4-5', 'value': 0.02},
                {'name': 'Advertising - Digital sensitivity', 'ts': '4-4-5', 'value': 0.32},
                {'name': 'Advertising - Partnership sensitivity', 'ts': '4-4-5', 'value': 0.09},
                {'name': 'Advertising - Print sensitivity', 'ts': '4-4-5', 'value': 0.15},
                {'name': 'Accumulation - TV', 'ts': '4-4-5', 'value': 2},
                {'name': 'Accumulation - Digital', 'ts': '4-4-5', 'value': 1},
                {'name': 'Accumulation - Partnership', 'ts': '4-4-5', 'value': 1},
                {'name': 'Accumulation - Print', 'ts': '4-4-5', 'value': 6},
                {'name': 'Lag - TV', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Digital', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Partnership', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Print', 'ts': '4-4-5', 'value': 1}
            ]
        },
        {
            'path': ['US', 'BAND-AID', 'PREMIUM'],
            'coefficients':[
                {'name': 'TDP Incrementality', 'ts': '4-4-5', 'value': 0.4},
                {'name': 'Everyday Price Elasticity', 'ts': '4-4-5', 'value': -0.25},
                {'name': 'Advertising - TV sensitivity', 'ts': '4-4-5', 'value': 0.03},
                {'name': 'Advertising - Digital sensitivity', 'ts': '4-4-5', 'value': 0},
                {'name': 'Advertising - Partnership sensitivity', 'ts': '4-4-5', 'value': 0.01},
                {'name': 'Advertising - Print sensitivity', 'ts': '4-4-5', 'value': 0.1},
                {'name': 'Accumulation - TV', 'ts': '4-4-5', 'value': 5},
                {'name': 'Accumulation - Digital', 'ts': '4-4-5', 'value': 0},
                {'name': 'Accumulation - Partnership', 'ts': '4-4-5', 'value': 4},
                {'name': 'Accumulation - Print', 'ts': '4-4-5', 'value': 6},
                {'name': 'Lag - TV', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Digital', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Partnership', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Print', 'ts': '4-4-5', 'value': 1}
            ]
        },
        {
            'path': ['US', 'BAND-AID', 'VALUE'],
            'coefficients': [
                {'name': 'TDP Incrementality', 'ts': '4-4-5', 'value': 0.4},
                {'name': 'Everyday Price Elasticity', 'ts': '4-4-5', 'value': -0.3},
                {'name': 'Advertising - TV sensitivity', 'ts': '4-4-5', 'value': 0.03},
                {'name': 'Advertising - Digital sensitivity', 'ts': '4-4-5', 'value': 0.07},
                {'name': 'Advertising - Partnership sensitivity', 'ts': '4-4-5', 'value': 0},
                {'name': 'Advertising - Print sensitivity', 'ts': '4-4-5', 'value': 0.08},
                {'name': 'Accumulation - TV', 'ts': '4-4-5', 'value': 5},
                {'name': 'Accumulation - Digital', 'ts': '4-4-5', 'value': 1},
                {'name': 'Accumulation - Partnership', 'ts': '4-4-5', 'value': 0},
                {'name': 'Accumulation - Print', 'ts': '4-4-5', 'value': 4},
                {'name': 'Lag - TV', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Digital', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Partnership', 'ts': '4-4-5', 'value': 0},
                {'name': 'Lag - Print', 'ts': '4-4-5', 'value': 1}
            ]
        },
    ]
}

dev_template_JJOralCare = {
    'tool_id': 1,
    'configuration': [
        {
            'name': 'available_dimensions',
            'value': [
                'geography', 'category',
            ]
        },
        {
            'name': 'dimension_geography_widget',
            'value': 'hierarchy'
        },
        {
            'name': 'dimension_category_widget',
            'value': 'hierarchy'
        }
    ],
    'top_entity': {},
    'entities': [
        ['US'], ['US', 'JJOralCare', 'Mouthwash'],
        ['Germany'], ['Germany', 'JJOralCare', 'Mouthwash'],
        ['UK'], ['UK', 'JJOralCare', 'Mouthwash'],
        ['Brazil'], ['Brazil', 'JJOralCare', 'Mouthwash'],
        ['Spain'], ['Spain', 'JJOralCare', 'Mouthwash'],
        ['Italy'], ['Italy', 'JJOralCare', 'Mouthwash'],
        ['Japan'], ['Japan', 'JJOralCare', 'Mouthwash'],
        ['Mexico'], ['Mexico', 'JJOralCare', 'Mouthwash'],
        ['Australia'], ['Australia', 'JJOralCare', 'Mouthwash'],
        ['Canada'], ['Canada', 'JJOralCare', 'Mouthwash']
    ],
    'timelines': {
        'names': ['annual'],
        'alias': {'history': {'annual': ('2012', '2015')},
                  'forecast': {'annual': ('2016', '2018')}},
        'top_ts_points': [
            {
                'name_full': '2012',
                'name_short': '2012',
                'children': []
            },
            {
                'name_full': '2012',
                'name_short': '2012',
                'children': []
            },
            {
                'name_full': '2013',
                'name_short': '2013',
                'children': []
            },
            {
                'name_full': '2014',
                'name_short': '2014',
                'children': []
            },
            {
                'name_full': '2015',
                'name_short': '2015',
                'children': []
            },
            {
                'name_full': '2016',
                'name_short': '2016',
                'children': []
            },
            {
                'name_full': '2017',
                'name_short': '2017',
                'children': []
            },
            {
                'name_full': '2018',
                'name_short': '2018',
                'children': []
            }
        ]
    },
    'structure': [
        {
            'meta': ('Geography', 'Country'),
            'variables': {
                'Population total': ['annual'],
                'CPI': ['annual'],
                'GDP PC': ['annual']
            },
            'coefficients': {}
        },
        {
            'meta': ('Products', 'Category'),
            'variables': {
                'Value': ['annual'],
                'EQ Volume': ['annual'],
                'Unit Volume': ['annual'],
                'Price per EQ': ['annual'],
                'Price per Unit': ['annual'],
                'Unit Size': ['annual'],
                'Distribution': ['annual'],
                'Innovation TDP share': ['annual'],
                'Premiumization': ['annual'],
                'Media Spend': ['annual'],
                'Avg % Discount': ['annual'],
                'Avg % Promo Support': ['annual'],
                'Avg % Volume sold as Promo': ['annual'],
                'LTT': ['annual']
            },
            'coefficients': {
                'Economy Sensitivity': ['annual'],
                'Innovations Sensitivity': ['annual'],
                'Regular Distribution Sensitivity': ['annual'],
                'Unit Price Elasticity': ['annual'],
                'Unit Size Elasticity': ['annual'],
                'Advertising Sensitivity': ['annual'],
                'Trade & Promo Sensitivity': ['annual']
            }
        }
    ],

    'exchange_rules': [
        {
            'meta': ('Geography', 'Country'),
            'input_variables': [
                {
                    'cont_var': 'Population total',
                    'cont_ts': 'annual',
                    'wh_var': 'Population, total',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'CPI',
                    'cont_ts': 'annual',
                    'wh_var': 'Consumer price index',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'GDP PC',
                    'cont_ts': 'annual',
                    'wh_var': 'GDP per capita, PPP exchange rate, real, US$',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                }
            ],
            'output_variables': []
        },
        {
            'meta': ('Products', 'Category'),
            'input_variables': [
                {
                    'cont_var': 'Value',
                    'cont_ts': 'annual',
                    'wh_var': 'Value Sales',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'EQ Volume',
                    'cont_ts': 'annual',
                    'wh_var': 'Volume Sales',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Unit Volume',
                    'cont_ts': 'annual',
                    'wh_var': 'Unit Sales',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Distribution',
                    'cont_ts': 'annual',
                    'wh_var': 'TDP',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Innovation TDP share',
                    'cont_ts': 'annual',
                    'wh_var': 'Innovation TDP share',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Premiumization',
                    'cont_ts': 'annual',
                    'wh_var': 'Premiumization',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend',
                    'cont_ts': 'annual',
                    'wh_var': 'Media Spend',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Avg % Discount',
                    'cont_ts': 'annual',
                    'wh_var': 'Avg % Discount',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Avg % Promo Support',
                    'cont_ts': 'annual',
                    'wh_var': 'Avg % Promo Support',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Avg % Volume sold as Promo',
                    'cont_ts': 'annual',
                    'wh_var': 'Avg % Volume sold as Promo',
                    'wh_ts': 'annual',
                    'time_period': 'history'
                }
            ],
            'output_variables': []
        }
    ],
    'dev_storage': [
        {
            'path': ['Germany', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.23},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.22},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.70},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.80},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.22},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.02},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.05}
            ]
        },
        {
            'path': ['Mexico', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.62},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.71},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.23},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.21},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.67},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.01}
            ]
        },
        {
            'path': ['US', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.16},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.08},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.03},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.27},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.70},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.01},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.35}
            ]
        },
        {
            'path': ['Brazil', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.25},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.43},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.14},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.35},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.05},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.01}
            ]
        },
        {
            'path': ['Italy', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.65},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.85},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.77},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.24},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.47},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.62}
            ]
        },
        {
            'path': ['Spain', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.25},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.96},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.13},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.20},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.12},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.67}
            ]
        },
        {
            'path': ['Australia', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.20},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.31},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.08},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.22},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.08},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.03},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.08}
            ]
        },
        {
            'path': ['Canada', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.21},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.10},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.05},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.44},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.42},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.06},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.67}
            ]
        },
        {
            'path': ['Japan', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.47},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.82},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.75},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.19},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.45},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.01}
            ]
        },
        {
            'path': ['UK', 'Mouthwash'],
            'coefficients': [
                {'name': 'Economy Sensitivity', 'ts': 'annual', 'value': 0.18},
                {'name': 'Innovations Sensitivity', 'ts': 'annual', 'value': 0.95},
                {'name': 'Regular Distribution Sensitivity', 'ts': 'annual', 'value': 0.09},
                {'name': 'Unit Price Elasticity', 'ts': 'annual', 'value': -0.50},
                {'name': 'Unit Size Elasticity', 'ts': 'annual', 'value': 0.13},
                {'name': 'Advertising Sensitivity', 'ts': 'annual', 'value': 0.08},
                {'name': 'Trade & Promo Sensitivity', 'ts': 'annual', 'value': 0.10}
            ]
        }

    ]
}