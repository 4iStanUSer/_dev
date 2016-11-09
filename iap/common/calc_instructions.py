
JJLean_queue_instructions = [
        {
            'name': 'forecast',
            'input_item': {'type': 2, 'meta_filter': ('Product', 'Segment')},
            'input_timescale': '4-4-5',
            'output_timescale': '4-4-5',
            'coefficients': [
                {
                    'meta': {'type': 0},
                    'data': [
                        'TDP Incrementality',
                        'Everyday Price Elasticity',
                        'Advertising - TV sensitivity',
                        'Advertising - Digital sensitivity',
                        'Advertising - Partnership sensitivity',
                        'Advertising - Print sensitivity',
                        'Accumulation - TV',
                        'Accumulation - Digital',
                        'Accumulation - Partnership',
                        'Accumulation - Print',
                        'Lag - TV',
                        'Lag - Digital',
                        'Lag - Partnership',
                        'Lag - Print'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Walmart']},
                    'data': [
                        'PPE',
                        'QM Lift',
                        'Promotion Discount',
                        'Promotion Support'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Target']},
                    'data': [
                        'PPE',
                        'QM Lift',
                        'Promotion Discount',
                        'Promotion Support'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Walgreens']},
                    'data': [
                        'PPE',
                        'QM Lift',
                        'Promotion Discount',
                        'Promotion Support'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['CVS']},
                    'data': [
                        'PPE',
                        'QM Lift',
                        'Promotion Discount',
                        'Promotion Support'
                    ]
                },
            ],
            'inputs': [
                {
                    'meta': {'type': 0},
                    'data': [
                        'Base Units',
                        'Base Units w/out impacts',
                        'TDP',
                        'Base Price',
                        'Media Spend - TV',
                        'Media Spend - Digital',
                        'Media Spend - Partnership',
                        'Media Spend - Print',
                        'TPR % Promo Support',
                        'TPR % Discount',
                        'Promo Price Elasticity',
                        'QM % Promo Support',
                        'QM % Discount',
                        'Quality Merch Lift',
                        'Consumption Coverage'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Walmart']},
                    'data': [
                        'Modeled Base Units',
                        'Display',
                        'Display parameters',
                        'Promo','Promo parameters'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Target']},
                    'data': [
                        'Modeled Base Units',
                        'Display',
                        'Display parameters',
                        'Promo',
                        'Promo parameters'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['Walgreens']},
                    'data': [
                        'Modeled Base Units',
                        'Display',
                        'Display parameters',
                        'Promo',
                        'Promo parameters'
                    ]
                },
                {
                    'meta': {'type': 2, 'path': ['CVS']},
                    'data': [
                        'Modeled Base Units',
                        'Display',
                        'Display parameters',
                        'Promo',
                        'Promo parameters'
                    ]
                }
            ],
            'output': ['Dollars', 'Units', 'Avg Price'],
            'scheme': {
                'inp_size': 44,
                'output': [],
                'modules': {
                    # Switch to get correct base units
                    '1': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 12},
                        'coefficients': [2,3,5],
                        'input_pins': [('inp', 0, True), ('13', 0, False)],
                        'out_size': 1
                    },
                    # Delay for Base units
                    '2': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 12},
                        'input_pins': [('1', 0, True)],
                        'out_size': 1
                    },
                    # Delay for TDP
                    '3': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 12},
                        'input_pins': [('inp', 2, True)],
                        'out_size': 1
                    },
                    # Lift for TDP
                    '4': {
                        'type': 'CM_LinearImpact',
                        'coefficients': [0],
                        'input_pins': [('3', 0, True), ('inp', 2, True)],
                        'out_size': 1
                    },
                    # Aggregated impact of TDP
                    '5': {
                        'type': 'CM_AutoSum',
                        'parameters': {'delay': 12},
                        'input_pins': [('2', 0, True), ('4', 0, True)],
                        'out_size': 1
                    },
                    # Delay for Base price
                    '6': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 12},
                        'input_pins': [('inp', 3, True)],
                        'out_size': 1
                    },
                    # Lift for base price
                    '7': {
                        'type': 'CM_ExponentialImpact',
                        'coefficients': [1],
                        'input_pins': [('6', 0, True), ('inp', 3, True)],
                        'out_size': 1
                    },
                    # Aggregated impact of base price
                    '8': {
                        'type': 'CM_AutoSum',
                        'parameters': {'delay': 12},
                        'input_pins': [('2', 0, True), ('7', 0, True)],
                        'out_size': 1
                    },
                    # TV adstock
                    '9': {
                        'type': 'CM_AdStockSimple',
                        'coefficients': [2, 6],
                        'input_pins': [('inp', 4, True)],
                        'out_size': 1
                    },
                    # Digital adstock
                    '10': {
                        'type': 'CM_AdStockSimple',
                        'coefficients': [3, 7],
                        'input_pins': [('inp', 5, True)],
                        'out_size': 1
                    },
                    # Partnership adstock
                    '11': {
                        'type': 'CM_AdStockSimple',
                        'coefficients': [4, 8],
                        'input_pins': [('inp', 6, True)],
                        'out_size': 1
                    },
                    # Print adstock
                    '12': {
                        'type': 'CM_AdStockSimple',
                        'coefficients': [5, 9],
                        'input_pins': [('inp', 7, True)],
                        'out_size': 1
                    },
                    # Sum Base units
                    '13': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('inp', 1, True),
                            ('5', 0, True),
                            ('8', 0, True),
                            ('9', 0, True),
                            ('10', 0, True),
                            ('11', 0, True),
                            ('12', 0, True)
                        ],
                        'out_size': 1
                    },
                    # TPR Promo price lift
                    '15': {
                        'type': 'CM_DiscountImpact',
                        'input_pins': [('inp', 9, True), ('inp', 10, True)],
                        'out_size': 1
                    },
                    # TPR Base Units
                    '16': {
                        'type': 'CM_Multiply',
                        'input_pins': [('inp', 8, True), ('13', 0, True)],
                        'out_size': 1
                    },
                    # TPR Units
                    '17': {
                        'type': 'CM_Multiply',
                        'input_pins': [('16', 0, True), ('15', 0, True)],
                        'out_size': 1
                    },
                    # QM Promo price lift
                    '18': {
                        'type': 'CM_DiscountImpact',
                        'input_pins': [('inp', 12, True), ('inp', 10, True)],
                        'out_size': 1
                    },
                    # Switch for base units
                    '19': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 1},
                        'input_pins': [('inp', 0, True), ('13', 0, False)],
                        'out_size': 1
                    },
                    # One tact delay for base units
                    '20': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('19', 0, True)],
                        'out_size': 1
                    },
                    # Change in total base units
                    '21': {
                        'type': 'CM_Divide',
                        'input_pins':[('13', 0, True), ('20', 0, True)],
                        'out_size': 1
                    },
                    # Walmart
                    # Switch between historical and modeled base units - Walmart
                    '22': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 1},
                        'input_pins': [('inp', 14, True), ('24', 0, False)],
                        'out_size': 1
                    },
                    # Delay for modeled base units - Walmart
                    '23': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('22', 0, True)],
                        'out_size': 1
                    },
                    # Modeled base units - Walmart
                    '24': {
                        'type': 'CM_Multiply',
                        'parameters': {},
                        'input_pins': [('21', 0, True), ('23', 0, True)],
                        'out_size': 1
                    },
                    # Calendar QM units and base units - Walmart
                    '25': {
                        'type': 'CM_PromoCalculator',
                        'coefficients': [14, 15, 16, 17],
                        'input_pins': [
                            ('24', 0, True),
                            ('inp', 15, True),
                            ('inp', 16, True),
                            ('inp', 17, True),
                            ('inp', 18, True),
                            ('inp', 19, True),
                            ('inp', 20, True)
                        ],
                        'out_size': 2
                    },
                    # Target
                    # Switch between historical and modeled base units - Target
                    '26': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 1},
                        'input_pins': [('inp', 21, True), ('28', 0, False)],
                        'out_size': 1
                    },
                    # Delay for modeled base units - Target
                    '27': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('26', 0, True)],
                        'out_size': 1
                    },
                    # Modeled base units - Target
                    '28': {
                        'type': 'CM_Multiply',
                        'input_pins': [('21', 0, True), ('27', 0, True)],
                        'out_size': 1
                    },
                    # Calendar QM units and base units - Target
                    '29': {
                        'type': 'CM_PromoCalculator',
                        'coefficients': [18, 19, 20, 21],
                        'input_pins': [
                            ('28', 0, True),
                            ('inp', 22, True),
                            ('inp', 23, True),
                            ('inp', 24, True),
                            ('inp', 25, True),
                            ('inp', 26, True),
                            ('inp', 27, True)
                        ],
                        'out_size': 2
                    },
                    # Walgreens
                    # Switch between historical and modeled base units - Walgreens
                    '30': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 1},
                        'input_pins': [('inp', 28, True), ('32', 0, False)],
                        'out_size': 1
                    },
                    # Delay for modeled base units - Walgreens
                    '31': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('30', 0, True)],
                        'out_size': 1
                    },
                    # Modeled base units - Walgreens
                    '32': {
                        'type': 'CM_Multiply',
                        'parameters': {},
                        'input_pins': [('21', 0, True), ('31', 0, True)],
                        'out_size': 1
                    },
                    # Calendar QM units and base units - Walgreens
                    '33': {
                        'type': 'CM_PromoCalculator',
                        'coefficients': [22, 23, 24, 25],
                        'input_pins': [
                            ('32', 0, True),
                            ('inp', 29, True),
                            ('inp', 30, True),
                            ('inp', 31, True),
                            ('inp', 32, True),
                            ('inp', 33, True),
                            ('inp', 34, True)
                        ],
                        'out_size': 2
                    },
                    # CVS
                    # Switch between historical and modeled base units - CVS
                    '34': {
                        'type': 'CM_Switch',
                        'parameters': {'runs_number': 1},
                        'input_pins': [('inp', 36, True), ('36', 0, False)],
                        'out_size': 1
                    },
                    # Delay for modeled base units - CVS
                    '35': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('34', 0, True)],
                        'out_size': 1
                    },
                    # Modeled base units - CVS
                    '36': {
                        'type': 'CM_Multiply',
                        'parameters': {},
                        'input_pins': [('21', 0, True), ('35', 0, True)],
                        'connected_modules': [],
                        'out_size': 1
                    },
                    # Calendar QM units and base units - CVS
                    '37': {
                        'type': 'CM_PromoCalculator',
                        'coefficients': [26, 27, 28, 29],
                        'input_pins': [
                            ('36', 0, True),
                            ('inp', 37, True),
                            ('inp', 38, True),
                            ('inp', 39, True),
                            ('inp', 40, True),
                            ('inp', 41, True),
                            ('inp', 42, True)
                        ],
                        'out_size': 2
                    },
                    # Total Calendar QM Base Units
                    '38': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('25', 0, True),
                            ('29', 0, True),
                            ('33', 0, True),
                            ('37', 0, True)
                        ],
                        'out_size': 1
                    },
                    # Total Calendar QM Units
                    '39': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('25', 1, True),
                            ('29', 1, True),
                            ('33', 1, True),
                            ('37', 1, True)
                        ],
                        'out_size': 1
                    },
                    # Total QM Base Units
                    '40': {
                        'type': 'CM_Multiply',
                        'input_pins': [
                            ('13', 0, True),
                            ('inp', 11, True)
                        ],
                        'out_size': 1
                    },
                    '41': {
                        'type': 'CM_Sum',
                        'input_pins': [('40', 0, True), ('38', 0, True)],
                        'out_size': 1
                    },
                    # Total QM Units
                    '42': {
                        'type': 'CM_Multiply',
                        'input_pins': [
                            ('13', 0, True),
                            ('inp', 11, True),
                            ('inp', 13, True),
                            ('18', 0, True)],
                        'out_size': 1
                    },
                    '43': {
                        'type': 'CM_Sum',
                        'input_pins': [('42', 0, True), ('39', 0, True)],
                        'out_size': 1
                    },
                    # Any Base Promo Units
                    '44': {
                        'type': 'CM_Sum',
                        'input_pins': [('16', 0, True), ('41', 0, True)],
                        'out_size': 1
                    },
                    # Any Promo Units
                    '45': {
                        'type': 'CM_Sum',
                        'input_pins': [('17', 0, True), ('43', 0, True)],
                        'out_size': 1
                    },
                    # Units
                    '46': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('13', 0, True),
                            ('44', 0, True),
                            ('45', 0, True)
                        ],
                        'out_size': 1
                    },
                    # Adjusted units
                    '47': {
                        'type': 'CM_Multiply',
                        'input_pins': [('46', 0, True), ('inp', 43, True)],
                        'out_size': 1
                    },
                    #Base dollars
                    #'': {
                    #    'type': 'CM_Divide',
                    #    'input_pins': [('13', 0, True), ('inp', 3, True)],
                    #    'out_size': 1
                    #},
                    # TRP base price
                    # TRP Dollars
                    # TRP Base Dollars
                    # QM base price
                    # Qm dollars
                    # QM base dollars
                    # any promo dollars, sum
                    # any promo base dollars
                    # dollars
                    # adjustment
                    # Price
                }
        }
    }]


JJOralCare_queue_instructions = {
    'top_queues': {
        'init': [
            {
                'name': 'main',
                'period': ['all']
            },
            {
                'name': 'growth_country',
                'period': ['growth_rates','history','forecast'],
            },
            {
                'name': 'growth_category',
                'period': ['growth_rates','history','forecast'],
            },
            {
                'name': 'decomposition',
                'period': ['growth_rates', 'history', 'forecast'],
            }
        ],
        'regular': [
            {
                'name': 'main',
                'period': ['all']
            },
        ],
        'cagr_for_period': [
            {
                'name': 'growth category'
            },
        ],
        'decomposition_for_period': [
            {
                'name': 'decomposition'
            },
        ]
    },
    'queues': [
        {
            'name': 'country_growth',
            'input_timescale': 'annual',
            'output_timescale': 'annual',
            'input_item': {'meta_filter': ('Geography', 'Country')},
            'input': [
                {
                    'meta': {'type': 0},
                    'data': [
                        ('Population total', 1),
                        ('CPI', 1),
                        ('GDP PC', 1)
                    ]
                },
            ],
            'controls': ['runs_count'],
            'parameters': {
                '1': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '2': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '3': {'var_type': 'abs', 'period_length': ('controls', 0)}
            },
            'modules': {
                '1': 'CM_Growth',
                '2': 'CM_Growth',
                '3': 'CM_Growth'
            },
            'input_pins': {
                '1': [('inp', 0, True)],
                '2': [('inp', 1, True)],
                '3': [('inp', 2, True)]
            },
            'output': [
                (('Population total', 4), ('1', 0)),
                (('CPI', 4), ('2', 0)),
                (('GDP PC', 4), ('3', 0))
            ]
        },
        {
            'name': 'category_growth',
            'input_timescale': 'annual',
            'output_timescale': 'annual',
            'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
            'input': [
                {
                    'meta': {'type': 0},
                    'data': [
                        ('EQ Volume', 1),
                        ('Unit Volume', 1),
                        ('Price per EQ', 1),
                        ('Price per Unit', 1),
                        ('Unit Size', 1),
                        ('Distribution', 1),
                        ('Innovation TDP share', 1),
                        ('Premiumization', 1),
                        ('Media Spend', 1),
                        ('Avg % Discount', 1),
                        ('Avg % Promo Support', 1),
                        ('LTT', 1)
                    ]
                }
            ],
            'controls': ['runs_count'],
            'parameters': {
                '1': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '2': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '3': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '4': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '5': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '6': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '7': {'var_type': 'rate', 'period_length': ('controls', 0)},
                '8': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '9': {'var_type': 'abs', 'period_length': ('controls', 0)},
                '10': {'var_type': 'rate', 'period_length': ('controls', 0)},
                '11': {'var_type': 'rate', 'period_length': ('controls', 0)},
                '12': {'var_type': 'rate', 'period_length': ('controls', 0)},
            },
            'modules': {
                '1': 'CM_Growth',
                '2': 'CM_Growth',
                '3': 'CM_Growth',
                '4': 'CM_Growth',
                '5': 'CM_Growth',
                '6': 'CM_Growth',
                '7': 'CM_Growth',
                '8': 'CM_Growth',
                '9': 'CM_Growth',
                '10': 'CM_Growth',
                '11': 'CM_Growth',
                '12': 'CM_Growth'
            },
            'input_pins': {
                '1': [('inp', 0, True)],
                '2': [('inp', 1, True)],
                '3': [('inp', 2, True)],
                '4': [('inp', 3, True)],
                '5': [('inp', 4, True)],
                '6': [('inp', 5, True)],
                '7': [('inp', 6, True)],
                '8': [('inp', 7, True)],
                '9': [('inp', 8, True)],
                '10': [('inp', 9, True)],
                '11': [('inp', 10, True)],
                '12': [('inp', 11, True)]
            },
            'output': [
                (('EQ Volume', 4), ('1', 0)),
                (('Unit Volume', 4), ('2', 0)),
                (('Price per EQ', 4), ('3', 0)),
                (('Price per Unit', 4), ('4', 0)),
                (('Unit Size', 4), ('5', 0)),
                (('Distribution', 4), ('6', 0)),
                (('Innovation TDP share', 4), ('7', 0)),
                (('Premiumization', 4), ('8', 0)),
                (('Media Spend', 4), ('9', 0)),
                (('Avg % Discount', 4), ('10', 0)),
                (('Avg % Promo Support', 4), ('11', 0)),
                (('LTT', 4),  ('12', 0))
            ],
        },
        {
            'name': 'decomposition',
            'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
            'input_timescale': 'annual',
            'output_timescale': 'annual',
            'input': [
                {
                    'meta': {'type': 0},
                    'data': [
                        ('Value', 1),
                        ('EQ Volume', 1),
                        ('dt_vol_Demographics', 1),
                        ('dt_vol_Economy', 1),
                        ('dt_vol_Innovative Distribution', 1),
                        ('dt_vol_Regular Distribution', 1),
                        ('dt_vol_Price-on-Volume changes', 1),
                        ('dt_vol_Unit Size changes', 1),
                        ('dt_vol_Advertizing', 1),
                        ('dt_vol_Discount changes', 1),
                        ('dt_vol_Promo Support changes', 1),
                        ('dt_vol_LTT', 1),
                        ('dt_pr_Inflation', 1),
                        ('dt_pr_Premiumization', 1),
                        ('dt_pr_Unit Size changes', 1),
                        ('dt_pr_Discount changes', 1),
                        ('dt_pr_Promo Support changes', 1),
                        ('dt_pr_Other', 1)
                    ]
                }
            ],
            'constants': [1],
            'parameters': {
                '1': {'delay': 1},
                '2': {'delay': 1}
            },
            'modules': {
                # CARGs for Value and Volume.
                '1': 'CM_Growth',
                '2': 'CM_Growth',
                # Delays for Value and Volume.
                '3': 'CM_Delay',
                '4': 'CM_Delay',
                # Value, Volume changes.
                '5': 'CM_Multiply',
                '6': 'CM_Multiply',
                '7': 'CM_Sum',
                '8': 'CM_Sum',
                '9': 'CM_CumulativeSum',
                '10': 'CM_CumulativeSum',
                # Demographic.
                '11': 'CM_Multiply',
                '12': 'CM_CumulativeSum',
                '13': 'CM_Divide',
                '14': 'CM_Multiply',
                # Economy.
                '15': 'CM_Multiply',
                '16': 'CM_CumulativeSum',
                '17':  'CM_Divide',
                '18': 'CM_Multiply',
                # Innovative deistribution.
                '19': 'CM_Multiply',
                '20': 'CM_CumulativeSum',
                '21': 'CM_Divide',
                '22': 'CM_Multiply',
                # Regular distribution.
                '23': 'CM_Multiply',
                '24': 'CM_CumulativeSum',
                '25': 'CM_Divide',
                '26': 'CM_Multiply',
                # Price on Volume.
                '27': 'CM_Multiply',
                '28': 'CM_CumulativeSum',
                '29': 'CM_Divide',
                '30': 'CM_Multiply',
                # Unit size.
                '31': 'CM_Multiply',
                '32': 'CM_CumulativeSum',
                '33': 'CM_Divide',
                '34': 'CM_Multiply',
                # Advertising.
                '35': 'CM_Multiply',
                '36': 'CM_CumulativeSum',
                '37': 'CM_Divide',
                '38': 'CM_Multiply',
                # Discount
                '39': 'CM_Multiply',
                '40': 'CM_CumulativeSum',
                '41': 'CM_Divide',
                '42': 'CM_Multiply',
                # Promo support.
                '43': 'CM_Multiply',
                '44': 'CM_CumulativeSum',
                '45': 'CM_Divide',
                '46': 'CM_Multiply',
                # Consumer trend.
                '47': 'CM_Multiply',
                '48': 'CM_CumulativeSum',
                '49': 'CM_Divide',
                '50': 'CM_Multiply',
                # Inflation on Price.
                '51': 'CM_Multiply',
                '52': 'CM_CumulativeSum',
                '53': 'CM_Divide',
                '54': 'CM_Multiply',
                # Premiumization on Price
                '55': 'CM_Multiply',
                '56': 'CM_CumulativeSum',
                '57': 'CM_Divide',
                '58': 'CM_Multiply',
                # Unit size on Price
                '59': 'CM_Multiply',
                '60': 'CM_CumulativeSum',
                '61': 'CM_Divide',
                '62': 'CM_Multiply',
                # Discount on Price
                '63': 'CM_Multiply',
                '64': 'CM_CumulativeSum',
                '65': 'CM_Divide',
                '66': 'CM_Multiply',
                # Promo Support on Price.
                '67': 'CM_Multiply',
                '68': 'CM_CumulativeSum',
                '69': 'CM_Divide',
                '70': 'CM_Multiply',
                # Other pricing drivers.
                '71': 'CM_Multiply',
                '72': 'CM_CumulativeSum',
                '73': 'CM_Divide',
                '74': 'CM_Multiply',
                # Trade & Promo
                '75': 'CM_Sum',
                '76': 'CM_Sum'
            },
            'input_pins': {
                # CARGs for Value and Volume.
                '1': [('inp', 0, True)],
                '2': [('inp', 1, True)],
                # Delays for Value and Volume.
                '3': [('inp', 0, True)],
                '4': [('inp', 1, True)],
                # Value, Volume changes.
                '5': [('1', 0, True), ('inp', 18, True)],
                '6': [('2', 0, True), ('inp', 18, True)],
                '7': [('inp', 0, True), ('5', 0, True)],
                '8':  [('inp', 1, True), ('6', 0, True)],
                '9':  [('7', 0, True)],
                '10': [('8', 0, True)],
                # Demographic.
                '11': [('4', 0, True), ('inp', 2, True)],
                '12': [('11', 0, True)],
                '13': [('12', 0, True), ('10', 0, True)],
                '14': [('2', 0, True), ('13', 0, True)],
                # Economy.
                '15': [('4', 0, True), ('inp', 3, True)],
                '16': [('15', 0, True)],
                '17': [('16', 0, True), ('10', 0, True)],
                '18': [('2', 0, True), ('17', 0, True)],
                # Innovative deistribution.
                '19': [('4', 0, True), ('inp', 4, True)],
                '20': [('19', 0, True)],
                '21': [('20', 0, True), ('10', 0, True)],
                '22': [('2', 0, True), ('21', 0, True)],
                # Regular distribution.
                '23': [('4', 0, True), ('inp', 5, True)],
                '24': [('23', 0, True)],
                '25': [('24', 0, True), ('10', 0, True)],
                '26': [('2', 0, True), ('25', 0, True)],
                # Price on Volume.
                '27': [('4', 0, True), ('inp', 6, True)],
                '28': [('27', 0, True)],
                '29': [('28', 0, True), ('10', 0, True)],
                '30': [('2', 0, True), ('29', 0, True)],
                # Unit size.
                '31': [('4', 0, True), ('inp', 7, True)],
                '32': [('31', 0, True)],
                '33': [('32', 0, True), ('10', 0, True)],
                '34': [('2', 0, True), ('33', 0, True)],
                # Advertising.
                '35': [('4', 0, True), ('inp', 8, True)],
                '36': [('35', 0, True)],
                '37': [('36', 0, True), ('10', 0, True)],
                '38': [('2', 0, True), ('37', 0, True)],
                # Discount
                '39': [('4', 0, True), ('inp', 9, True)],
                '40': [('39', 0, True)],
                '41': [('40', 0, True), ('10', 0, True)],
                '42': [('2', 0, True), ('41', 0, True)],
                # Promo support.
                '43': [('4', 0, True), ('inp', 10, True)],
                '44': [('43', 0, True)],
                '45': [('44', 0, True), ('10', 0, True)],
                '46': [('2', 0, True), ('45', 0, True)],
                # Consumer trend.
                '47': [('4', 0, True), ('inp', 11, True)],
                '48': [('47', 0, True)],
                '49': [('48', 0, True), ('10', 0, True)],
                '50': [('2', 0, True), ('49', 0, True)],
                # Inflation on Price.
                '51': [('3', 0, True), ('inp', 12, True)],
                '52': [('51', 0, True)],
                '53': [('52', 0, True), ('9', 0, True)],
                '54': [('1', 0, True), ('53', 0, True)],
                # Premiumization on Price
                '55': [('3', 0, True), ('inp', 13, True)],
                '56': [('55', 0, True)],
                '57': [('56', 0, True), ('9', 0, True)],
                '58': [('1', 0, True), ('57', 0, True)],
                # Unit size on Price
                '59': [('3', 0, True), ('inp', 14, True)],
                '60': [('59', 0, True)],
                '61': [('60', 0, True), ('9', 0, True)],
                '62': [('1', 0, True), ('61', 0, True)],
                # Discount on Price
                '63': [('3', 0, True), ('inp', 15, True)],
                '64': [('63', 0, True)],
                '65': [('64', 0, True), ('9', 0, True)],
                '66': [('1', 0, True), ('65', 0, True)],
                # Promo Support on Price.
                '67': [('3', 0, True), ('inp', 16, True)],
                '68': [('67', 0, True)],
                '69': [('68', 0, True), ('9', 0, True)],
                '70': [('1', 0, True), ('69', 0, True)],
                # Other pricing drivers.
                '71': [('3', 0, True), ('inp', 17, True)],
                '72': [('71', 0, True)],
                '73': [('72', 0, True), ('9', 0, True)],
                '74': [('1', 0, True), ('73', 0, True)]
            },
            'output': [
                (('dec_val_Demographic', 4), ('14', 0)),
                (('dec_val_Economy', 4),  ('18', 0)),
                (('dec_val_Distribution', 4), ('26', 0)),
                (('dec_val_Innovation', 4), ('22', 0)),
                (('dec_val_Advertising', 4), ('38', 0)),
                (('dec_val_Trade & Promo-on-Volume', 4), ('75', 0)),
                (('dec_val_Price-on-Volume Impact', 4), ('30', 0)),
                (('dec_val_UnitSize-on-Volume Impact', 4), ('34', 0)),
                (('dec_val_Inflation', 4), ('54', 0)),
                (('dec_val_Manufacturer Pricing', 4), ('74', 0)),
                (('dec_val_Premiumization', 4), ('58', 0)),
                (('dec_val_Trade & Promo', 4), ('76', 0)),
                (('dec_val_Unit Size', 4), ('62', 0)),
                (('dec_vol_Demographic', 4), ('14', 0)),
                (('dec_vol_Economy', 4), ('18', 0)),
                (('dec_vol_Distribution', 4), ('26', 0)),
                (('dec_vol_Innovation', 4), ('22', 0)),
                (('dec_vol_Advertising', 4), ('38', 0)),
                (('dec_vol_Trade & Promo', 4), ('75', 0)),
                (('dec_vol_Price-on-Volume Impact', 4), ('30', 0)),
                (('dec_vol_UnitSize-on-Volume Impact', 4),('34', 0)),
                (('dec_vol_Long Term Trend', 4), ('50', 0))
            ]
        },
        {
            'name': 'main',
            'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
            'input_timescale': 'annual',
            'output_timescale': 'annual',
            'input': [
                {
                    'meta': {'type': 3, 'meta_filter': ('Geography', 'Country')},
                    'data': [
                        ('Population total', 1),
                        ('CPI', 1),
                        ('GDP PC', 1)
                    ]
                },
                {
                    'meta': {'type': 0},
                    'data': [
                        ('EQ Volume', 1),
                        ('Price per Unit',  1),
                        ('Unit Size', 1),
                        ('Distribution', 1),
                        ('Innovation TDP share', 1),
                        ('Premiumization', 1),
                        ('Media Spend', 1),
                        ('Avg % Discount', 1),
                        ('Avg % Promo Support', 1),
                        ('Avg % Volume sold as Promo', 1),
                        ('LTT', 1)
                    ],
                    'coefficients':[
                        ('Economy Sensitivity', 2),
                        ('Innovations Sensitivity', 2),
                        ('Regular Distribution Sensitivity', 2),
                        ('Unit Price Elasticity', 2),
                        ('Unit Size Elasticity', 2),
                        ('Advertising Sensitivity', 2),
                        ('Trade & Promo Sensitivity', 2),
                    ]
                }
            ],
            'constants': [1, -1],
            'controls': ['last_actual'],
            'parameters': {
                # Due to Demographics.
                '1': {'start': ('controls', 0), 'delay': 1},
                '2': {'start': ('controls', 0), 'sensitivity': 1, 'type': 'linear', 'var_type': 'abs'},
                # Due to Economy.
                '3': {'start': ('controls', 0), 'delay': 1},
                '4': {'start': ('controls', 0), 'sensitivity': ('coefficients', 0), 'type': 'linear', 'var_type': 'abs'},
                # Due to Unit Size changes.
                '5': {'start': ('controls', 0), 'delay': 1},
                '6': {'start': ('controls', 0), 'sensitivity': ('coefficients', 4), 'type': 'exp', 'var_type': 'abs'},
                '7': {'start': ('controls', 0), 'sensitivity': ('coefficients', 4), 'type': 'linear', 'var_type': 'abs'},
                # Due to Inflation.
                '8': {'start': ('controls', 0), 'delay': 1},
                '9': {'start': ('controls', 0), 'sensitivity': 1, 'type': 'linear', 'var_type': 'abs'},
                # Due to Premiumization.
                '10': {'start': ('controls', 0), 'delay': 1},
                '11': {'start': ('controls', 0), 'sensitivity': 1, 'type': 'linear', 'var_type': 'abs'},
                # Due to Advertizing.
                '12': {'start': ('controls', 0), 'delay': 1},
                '13': {'start': ('controls', 0), 'sensitivity': ('coefficients', 5),'type': 'linear', 'above_count': 1},
                # Due to distribution.
                '14': {'start': ('controls', 0), 'delay': 1},
                '15': {'start': ('controls', 0), 'delay': 1},
                '16': {'start': ('controls', 0), 'regular_sensitivity': ('coefficients', 2), 'innovations_sensitivity': ('coefficients', 1)},
                # Delay for Volume sold as promo.
                '17': {'start': ('controls', 0), 'delay': 1},
                # Due to Discount.
                '18': {'start': 0, 'delay': 1},
                '19': {'start': 0, 'sensitivity': ('coefficients', 6), 'type': 'linear', 'var_type': 'rate'},
                '20': {'start': 0},
                '21': {'start': ('controls', 0)},
                # Due to Promo Support.
                '22': {'start': 0, 'delay': 1},
                '23': {'start': 0, 'sensitivity': ('coefficients', 6), 'type': 'linear', 'var_type': 'rate'},
                '24': {'start': 0},
                '25': {'start': ('controls', 0)},
                # Due to Price.
                '26': {'start': ('controls', 0), 'delay': 1},
                '27': {'start': ('controls', 0), 'sensitivity': ('coefficients', 3)},
                # Due to Other Pricing drivers
                '28': {'start': ('controls', 0)},
                '29': {'start': ('controls', 0), 'delay': 1},
                '30': {'start': ('controls', 0)},
                '31': {'start': ('controls', 0)},
                '32': {'start': ('controls', 0)},
                '33': {'start': ('controls', 0)},
                # Forecasting Volume
                '34': {'start': ('controls', 0)},
                '35': {'start': ('controls', 0), 'delay': 1},
                '36': {'start': ('controls', 0)},
                # Sales Value
                '37': {'start': ('controls', 0)},
                # Sales Units
                '38': {'start': ('controls', 0)},
            },
            'modules': {
                # Due to Demographics.
                '1': 'CM_Delay',
                '2': 'CM_Impact',
                # Due to Economy.
                '3': 'CM_Delay',
                '4': 'CM_Impact',
                # Due to Unit Size changes.
                '5': 'CM_Delay',
                '6': 'CM_Impact',
                '7': 'CM_Impact',
                # Due to Inflation.
                '8': 'CM_Delay',
                '9': 'CM_Impact',
                # Due to Premiumization.
                '10': 'CM_Delay',
                '11': 'CM_Impact',
                # Due to Advertizing.
                '12': 'CM_Delay',
                '13': 'CM_ImpactAbove',
                # Due to distribution.
                '14': 'CM_Delay',
                '15': 'CM_Delay',
                '16': 'CM_JJOralCare_DistributionImpact',
                # Delay for Volume sold as promo.
                '17': 'CM_Delay',
                # Due to Discount.
                '18': 'CM_Delay',
                '19': 'CM_Impact',
                '20': 'CM_CumulativeAverage',
                '21': 'CM_JJOralCare_DiscountOnPriceImpact',
                # Due to Promo Support.
                '22': 'CM_Delay',
                '23': 'CM_Impact',
                '24': 'CM_CumulativeAverage',
                '25': 'CM_JJOralCare_PromoOnPriceImpact',
                # Due to Price.
                '26': 'CM_Delay',
                '27': 'CM_JJOralCare_PriceImpact',
                # Due to Other Pricing drivers
                '28': 'CM_Divide',
                '29': 'CM_Delay',
                '30': 'CM_Growth',
                '31': 'CM_Sum',
                '32': 'CM_Multiply',
                '33': 'CM_Sum',
                # Forecasting Volume
                '34': 'CM_Sum',
                '35': 'CM_Delay_Switch',
                '36': 'CM_Multiply',
                # Sales Value
                '37': 'CM_Multiply',
                # Sales Units
                '38': 'CM_Divide'
            },
            'input_pins': {
                # Due to Demographics.
                '1': [('inp', 0, True)],
                '2': [('inp', 0, True), ('1', 0, True)],
                # Due to Economy.
                '3': [('inp', 2, True)],
                '4': [('inp', 2, True), ('3', 0, True)],
                # Due to Unit Size changes.
                '5': [('inp', 5, True)],
                '6': [('inp', 5, True), ('5', 0, True)],
                '7': [('inp', 5, True), ('5', 0, True)],
                # Due to Inflation.
                '8': [('inp', 1, True)],
                '9': [('inp', 1, True), ('8', 0, True)],
                # Due to Premiumization.
                '10': [('inp', 8, True)],
                '11': [('inp', 8, True), ('10', 0, True)],
                # Due to Advertizing.
                '12': [('inp', 9, True)],
                '13': [('inp', 9, True), ('12', 0, True), ('inp', 1, True), ('8', 0, True)],
                # Due to distribution.
                '14': [('inp', 6, True)],
                '15': [('inp', 7, True)],
                '16': [('inp', 6, True), ('14', 0, True), ('inp', 7, True), ('15', 0, True)],
                # Delay for Volume sold as promo.
                '17': [('inp', 12, True)],
                # Due to Discount.
                '18': [('inp', 10, True)],
                '19': [('inp', 10, True), ('18', 0, True)],
                '20': [('19', 0, True)],
                '21': [('inp', 10, True), ('18', 0, True), ('17', 0, True), ('20', 0, True)],
                # Due to Promo Support.
                '22': [('inp', 11, True)],
                '23': [('inp', 11, True), ('22', 0, True)],
                '24': [('23', 0, True)],
                '25': [('inp', 10, True), ('18', 0, True), ('17', 0, True), ('23', 0, True)],
                # Due to Price.
                '26': [('inp', 4, True)],
                '27': [
                    ('inp', 4, True), ('26', 0, True), ('inp', 8, True),
                    ('10', 0, True), ('inp', 1, True), ('8', 0, True),
                    ('21', 0, True), ('25', 0, True), ('20', 0, True),
                    ('24', 0, True)
                ],
                # Due to Other Pricing drivers
                '28': [('inp', 4, True), ('inp', 5, True)],
                '29': [('28', 0, True)],
                '30': [('28', 0, True), ('29', 0, True)],
                '31': [('9', 0, True), ('11', 0, True), ('7', 0, True), ('21', 0, True), ('25', 0, True)],
                '32': [('31', 0, True), ('inp', 15, True)],
                '33': [('30', 0, True), ('32', 0, True)],
                # Forecasting Volume
                '34': [
                    ('2', 0, True),
                    ('4', 0, True),
                    ('6', 0, True),
                    ('13', 0, True),
                    ('16', 0, True),
                    ('16', 1, True),
                    ('19', 0, True),
                    ('23', 0, True),
                    ('27', 0, True),
                    ('inp', 13, True),
                    ('inp', 14, True)
                ],
                '35': [('inp', 3, True), ('36', 0, False)],
                '36': [('34', 0, True), ('35', 0, True)],
                # Sales Value
                '37': [('36', 0, True), ('28', 0, True)],
                # Sales Units
                '38': [('36', 0, True), ('inp', 5, True)]
            },
            'output': [
                (('Value', 1), ('37', 0)),
                (('EQ Volume', 1), ('36', 0)),
                (('Unit Volume', 1), ('38', 0)),
                (('Price per EQ', 1), ('28', 0)),
                (('dt_vol_Demographics', 1), ('2', 0)),
                (('dt_vol_Economy', 1),  ('4', 0)),
                (('dt_vol_Innovative Distribution', 1), ('16', 0)),
                (('dt_vol_Regular Distribution', 1), ('16', 1)),
                (('dt_vol_Price-on-Volume changes', 1), ('27', 0)),
                (('dt_vol_Unit Size changes', 1), ('6', 0)),
                (('dt_vol_Advertizing', 1), ('13', 0)),
                (('dt_vol_Discount changes', 1), ('19', 0)),
                (('dt_vol_Promo Support changes', 1), ('23', 0)),
                (('dt_vol_LTT', 1), ('inp', 13)),
                (('dt_pr_Inflation', 1), ('9', 0)),
                (('dt_pr_Premiumization', 1), ('11', 0)),
                (('dt_pr_Unit Size changes', 1), ('7', 0)),
                (('dt_pr_Discount changes', 1), ('21', 0)),
                (('dt_pr_Promo Support changes', 1), ('25', 0)),
                (('dt_pr_Other', 1), ('33', 0))
            ]
        }
    ]
}
