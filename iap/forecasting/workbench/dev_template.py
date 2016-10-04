dev_template = {
    'top_entity': {'path': ['US']},
    'timescales': {
        'annual': ['2011', '2012', '2013', '2014', '2015', '2016',
                   '2017'],
        '4-4-5': [
            'Jan-11', 'Feb-11', 'Jan-11', 'Feb-11', 'Mar-11', 'Apr-11',
            'May-11', 'Jun-11', 'Jul-11', 'Aug-11' 'Sep-11', 'Oct-11',
            'Nov-11', 'Dec-11', 'Jan-12', 'Feb-12', 'Jan-12', 'Feb-12',
            'Mar-12', 'Apr-12', 'May-12', 'Jun-12', 'Jul-12', 'Aug-12',
            'Sep-12', 'Oct-12', 'Nov-12', 'Dec-12', 'Jan-13', 'Feb-13',
            'Jan-13', 'Feb-13', 'Mar-13', 'Apr-13', 'May-13', 'Jun-13',
            'Jul-13', 'Aug-13', 'Sep-13', 'Oct-13', 'Nov-13', 'Dec-13',
            'Jan-14', 'Feb-14', 'Jan-14', 'Feb-14', 'Mar-14', 'Apr-14',
            'May-14', 'Jun-14', 'Jul-14', 'Aug-14', 'Sep-14', 'Oct-14',
            'Nov-14', 'Dec-14', 'Jan-15', 'Feb-15', 'Jan-15', 'Feb-15',
            'Mar-15', 'Apr-15', 'May-15', 'Jun-15', 'Jul-15', 'Aug-15',
            'Sep-15', 'Oct-15', 'Nov-15', 'Dec-15', 'Jan-16', 'Feb-16',
            'Jan-16', 'Feb-16', 'Mar-16', 'Apr-16', 'May-16', 'Jun-16',
            'Jul-16', 'Aug-16', 'Sep-16', 'Oct-16', 'Nov-16', 'Dec-16',
            'Jan-17', 'Feb-17', 'Jan-17', 'Feb-17', 'Mar-17', 'Apr-17',
            'May-17', 'Jun-17', 'Jul-17', 'Aug-17', 'Sep-17', 'Oct-17',
            'Nov-17', 'Dec-17']
        },
    'structure': [
        {
            'meta': ('Geography', 'Country'),
            'variables': [],
            'coefficients': []
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
            'meta': ('Products', 'Segment'),
            'input_variables': [
                {
                    'cont_var': 'Media Spend - TV',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Media Spend - TV',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Digital',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Media Spend - Digital',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Partnership',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Media Spend - Partnership',
                    'wh_ts': '4-4-5',
                    'time_period': 'history'
                },
                {
                    'cont_var': 'Media Spend - Print',
                    'cont_ts': '4-4-5',
                    'wh_var': 'Media Spend - Print',
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
            ]
        },
        {
            'meta': ('Products', 'Segment'),
            'variables': [
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
            ]
        },
        {
            'meta': ('Chanel Distribution', 'Chanel'),
            'variables': [
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
            ]
        }
    ],
    'dev_storage': [
        {
            'path': ['US', 'Band-Aid', 'Decorated'],
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
            'path': ['US', 'Band-Aid', 'Premium'],
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
            'path': ['US', 'Band-Aid', 'Value'],
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
            'path': ['US', 'Band-Aid', 'Decorated', 'Wal-mart'],
            'coefficients': {
                'PPE': {'New @ $XX': -1.10, 'Buy @ $XX': -1.10, 'ADS': -1.10},
                'QM Lift': {'New @ $XX': 1.15, 'Buy @ $XX': 1.06, 'ADS': 1.20},
                'Promotion Discount': {'New @ $XX': 0, 'Buy @ $XX': 0, 'ADS': 0},
                'Promotion Support': {'New @ $XX': 0.42, 'Buy @ $XX': 0.41,'ADS': 0.41}
            }
        },
        {
            'path': ['US', 'Band-Aid', 'Premium', 'Wal-mart'],
            'coefficients': {
                'PPE': {'Buy @ $XX': -1.3, 'ADS': -1.3},
                'QM Lift': {'Buy @ $XX': 1.19, 'ADS': 1.4},
                'Promotion Discount': {'Buy @ $XX': 0.01, 'ADS': 0.01},
                'Promotion Support': {'Buy @ $XX': 0.1,'ADS': 0.1}
            }
        },
        {
            'path': ['US', 'Band-Aid', 'Value', 'Wal-mart'],
            'coefficients': {
                'PPE': {'ADS': -1.3},
                'QM Lift': {'ADS': 1.4},
                'Promotion Discount': {'ADS': 0.01},
                'Promotion Support': {'ADS': 0.1}
            }
        }
    ]
}