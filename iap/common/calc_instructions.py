
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


JJOralCare_queue_instructions = [
    {
        'id': 'due_tos',
        'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
        'input_timescale': 'annual',
        'output_timescale': 'annual',
        'input': [
            {
                'meta': {'type': 4},
                'data': [1]
            },
            {
                'meta': {'type': 3, 'meta_filter': ('Geography', 'Country')},
                'data': [
                    ('Population total', 'annual', 1),
                    ('CPI', 'annual', 1),
                    ('GDP PC', 'annual', 1)
                ]
            },
            {
                'meta': {'type': 0},
                'data': [
                    ('EQ Volume', 'annual', 1),
                    ('Unit Volume', 'annual', 1),
                    ('Price per EQ', 'annual', 1),
                    ('Price per Unit', 'annual', 1),
                    ('Unit Size', 'annual', 1),
                    ('Distribution', 'annual', 1),
                    ('Innovation TDP share', 'annual', 1),
                    ('Premiumization', 'annual', 1),
                    ('Media Spend', 'annual', 1),
                    ('Avg % Discount', 'annual', 1),
                    ('Avg % Promo Support', 'annual', 1),
                    ('Avg % Volume sold as Promo', 'annual', 1),
                    ('LTT', 'annual', 1),
                    ('Above Unit Price', 'annual', 1),
                    ('Economy Sensitivity', 'annual', 2),
                    ('Innovations Sensitivity', 'annual', 2),
                    ('Regular Distribution Sensitivity', 'annual', 2),
                    ('Unit Price Elasticity', 'annual', 2),
                    ('Unit Size Elasticity', 'annual', 2),
                    ('Advertising Sensitivity', 'annual', 2),
                    ('Trade & Promo Sensitivity', 'annual', 2),
                ]
            }

        ],
        'output': [
            'Value',
            'EQ Volume',
            'Unit Volume',
            'Price per EQ'
            'Due to Demographics',
            'Due to Economy',
            'Due to Innovative Distribution',
            'Due to Regular Distribution',
            'Due to Price-on-Volume changes',
            'Due to Unit Size changes',
            'Due to Advertizing',
            'Due to Discount changes',
            'Due to Promo Support changes',
            'Due to Inflation',
            'Due to Premiumization',
            'Due to Unit Size changes',
            'Due to Discount changes',
            'Due to Promo Support changes'
        ],
        'scheme': {
            'output': [('25', 0), ('23', 0), ('26', 0), ('24', 0)],
            'constants': [1],
            'modules': {
                # Due to Demographics.
                '1': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 0, True)],
                    'out_size': 1
                },
                '2': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'linear', 'var_type': 'abs'},
                    'coefficients': [7],
                    'input_pins': [('inp', 0, True), ('1', 0, True)],
                    'out_size': 1
                },
                # Due to Economy.
                '3': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 2, True)],
                    'out_size': 1
                },
                '4': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'linear', 'var_type': 'abs'},
                    'coefficients': [0],
                    'input_pins': [('inp', 2, True), ('3', 0, True)],
                    'out_size': 1
                },
                # Due to Unit Size changes.
                '5': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 7, True)],
                    'out_size': 1
                },
                '6': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'exp', 'var_type': 'abs'},
                    'coefficients': [4],
                    'input_pins': [('inp', 7, True), ('5', 0, True)],
                    'out_size': 1
                },
                '7': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'linear', 'var_type': 'abs'},
                    'coefficients': [4],
                    'input_pins': [('inp', 7, True), ('5', 0, True)],
                    'out_size': 1
                },
                # Due to Inflation.
                '8': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 1, True)],
                    'out_size': 1
                },
                '9': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'linear', 'var_type': 'abs'},
                    'coefficients': [4],
                    'input_pins': [('inp', 1, True), ('8', 0, True)],
                    'out_size': 1
                },
                # Due to Premiumization.
                '10': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 10, True)],
                    'out_size': 1
                },
                '11': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'linear', 'var_type': 'abs'},
                    'coefficients': [4],
                    'input_pins': [('inp', 10, True), ('10', 0, True)],
                    'out_size': 1
                },
                # Due to Advertizing.
                '12': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 11, True)],
                    'out_size': 1
                },
                '13': {
                    'type': 'CM_ImpactAbove',
                    'parameters': {'type': 'linear', 'above_count': 1},
                    'coefficients': [5],
                    'input_pins': [('inp', 11, True), ('12', 0, True),
                                   ('inp', 1, True), ('8', 0, True)],
                    'out_size': 1
                },
                # Discount changes.

                '14': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 12, True)],
                    'out_size': 1
                },
                '15': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'exp', 'var_type': 'rate'},
                    'coefficients': [6],
                    'input_pins': [('inp', 12, True), ('14', 0, True)],
                    'out_size': 1
                },
                '16': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 14, True)],
                    'out_size': 1
                },
                '17': {
                    'type': 'CM_JJOralCare_Discount_on_price_impact',
                    'input_pins': [(), ('inp', 14, True)],
                    'out_size': 1
                },



                # Promo Support.
                '12': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 13, True)],
                    'out_size': 1
                },
                '13': {
                    'type': 'CM_Impact',
                    'parameters': {'type': 'exp', 'var_type': 'rate'},
                    'coefficients': [6],
                    'input_pins': [('inp', 13, True), ('12', 0, True)],
                    'out_size': 1
                },
                # Due to Innovative Distribution.
                # Due to Regular Distribution.
                '14': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 8, True)],
                    'out_size': 1
                },
                '15': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 9, True)],
                    'out_size': 1
                },
                '16': {
                    'type': 'CM_JJOralCare_DistributionImpact',
                    'coefficients': [2, 1],
                    'input_pins': [('inp', 8, True), ('14', 0, True),
                                   ('inp', 9, True), ('15', 0, True)],
                    'out_size': 2
                },
                # Pricing.
                '17': {
                    'type': 'CM_Delay',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 6, True)],
                    'out_size': 1
                },

                '19': {
                    'type': 'CM_JJOralCare_PriceImpact',
                    'parameters': {'type': 'exp', 'above_count': 2},
                    'coefficients': [5],
                    'input_pins': [('inp', 6, True), ('17', 0, True),
                                   ('inp', 10, True), ('18', 0, True),
                                   ('inp', 1, True), ('8', 0, True),
                                   ('inp', 15, True)],
                    'out_size': 1
                },
                # Sum Lifts.
                '20': {
                    'type': 'CM_Sum',
                    'input_pins': [
                        ('2', 0, True),
                        ('4', 0, True),
                        ('6', 0, True),
                        ('9', 0, True),
                        ('11', 0, True),
                        ('13', 0, True),
                        ('16', 0, True),
                        ('19', 0, True),
                        ('inp', 14, True)
                    ],
                    'out_size': 1
                },
                '21': {
                    'type': 'CM_Sum',
                    'input_pins': [
                        ('20', 0, True),
                        ('const', 0, True)
                    ],
                    'out_size': 1
                },
                # EQ Volume
                '22': {
                    'type': 'CM_Delay_Switch',
                    'parameters': {'delay': 1},
                    'input_pins': [('inp', 3, True), ('23', 0, False)],
                    'out_size': 1
                },



                '23': {
                    'type': 'CM_Multiply',
                    'input_pins': [('21', 0, True), ('22', 0, True)],
                    'out_size': 1
                },
                # Price Per EQ
                '24': {
                    'type': 'CM_Divide',
                    'input_pins':[('inp', 6, True), ('inp', 7, True)],
                    'out_size': 1
                },
                # Sales Value
                '25': {
                    'type': 'CM_Multiply',
                    'input_pins': [('23', 0, True), ('24', 0, True)],
                    'out_size': 1
                },
                # Sales Units
                '26': {
                    'type': 'CM_Divide',
                    'input_pins': [('22', 0, True), ('inp', 7, True)],
                    'out_size': 1
                }
            }
        }


    },

        {
            'name': 'forecast',
            'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
            'input_timescale': 'annual',
            'output_timescale': 'annual',
            'period': ('2015', '2018'),
            'coefficients': [
                {
                    'meta': {'type': 0},
                    'data': [
                        ('Economy Sensitivity', 'annual'),
                        ('Innovations Sensitivity', 'annual'),
                        ('Regular Distribution Sensitivity', 'annual'),
                        ('Unit Price Elasticity', 'annual'),
                        ('Unit Size Elasticity', 'annual'),
                        ('Advertising Sensitivity', 'annual'),
                        ('Trade & Promo Sensitivity', 'annual'),
                    ]
                },
                {
                    'meta': {'type': 4},
                    'data': [1]
                }
            ],
            'inputs': [
                {
                    'meta': {'type': 3, 'meta_filter': ('Geography', 'Country')},
                    'data': [
                        'Population total',
                        'CPI',
                        'GDP PC'
                    ]
                },
                {
                    'meta': {'type': 0},
                    'data': [
                        'EQ Volume',
                        'Unit Volume',
                        'Price per EQ',
                        'Price per Unit',
                        'Unit Size',
                        'Distribution',
                        'Innovation TDP share',
                        'Premiumization',
                        'Media Spend',
                        'Avg % Discount',
                        'Avg % Promo Support',
                        'LTT',
                        'Above Unit Price'
                    ]
                }
            ],
            'output': ['Value', 'EQ Volume', 'Unit Volume', 'Price per EQ'],
            'scheme': {
                'inp_size': 16,
                'output': [('25', 0), ('23', 0), ('26', 0), ('24', 0)],
                'constants': [1],
                'modules': {
                    # Demographics.
                    '1': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 0, True)],
                        'out_size': 1
                    },
                    '2': {
                        'type': 'CM_Impact',
                        'parameters': {'type': 'linear', 'var_type': 'abs'},
                        'coefficients': [7],
                        'input_pins': [('inp', 0, True), ('1', 0, True)],
                        'out_size': 1
                    },
                    # Economy.
                    '3': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 2, True)],
                        'out_size': 1
                    },
                    '4': {
                        'type': 'CM_Impact',
                        'parameters': {'type': 'linear', 'var_type': 'abs'},
                        'coefficients': [0],
                        'input_pins': [('inp', 2, True), ('3', 0, True)],
                        'out_size': 1
                    },
                    # Unit size.
                    '5': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 7, True)],
                        'out_size': 1
                    },
                    '6': {
                        'type': 'CM_Impact',
                        'parameters': {'type': 'exp', 'var_type': 'abs'},
                        'coefficients': [4],
                        'input_pins': [('inp', 7, True), ('5', 0, True)],
                        'out_size': 1
                    },
                    # Advertising.
                    '7': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 11, True)],
                        'out_size': 1
                    },
                    '8': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 1, True)],
                        'out_size': 1
                    },
                    '9': {
                        'type': 'CM_ImpactAbove',
                        'parameters': {'type': 'linear', 'above_count': 1},
                        'coefficients': [5],
                        'input_pins': [('inp', 11, True), ('7', 0, True),
                                       ('inp', 1, True), ('8', 0, True)],
                        'out_size': 1
                    },
                    # Discount changes.
                    '10': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 12, True)],
                        'out_size': 1
                    },
                    '11': {
                        'type': 'CM_Impact',
                        'parameters': {'type': 'exp', 'var_type': 'rate'},
                        'coefficients': [6],
                        'input_pins': [('inp', 12, True), ('10', 0, True)],
                        'out_size': 1
                    },
                    # Promo Support.
                    '12': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 13, True)],
                        'out_size': 1
                    },
                    '13': {
                        'type': 'CM_Impact',
                        'parameters': {'type': 'exp', 'var_type': 'rate'},
                        'coefficients': [6],
                        'input_pins': [('inp', 13, True), ('12', 0, True)],
                        'out_size': 1
                    },
                    # Distribution
                    '14': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 8, True)],
                        'out_size': 1
                    },
                    '15': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 9, True)],
                        'out_size': 1
                    },
                    '16': {
                        'type': 'CM_JJOralCare_DistributionImpact',
                        'coefficients': [2, 1],
                        'input_pins': [('inp', 8, True), ('14', 0, True),
                                       ('inp', 9, True), ('15', 0, True)],
                        'out_size': 1
                    },
                    # Pricing.
                    '17': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 6, True)],
                        'out_size': 1
                    },
                    '18': {
                        'type': 'CM_Delay',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 10, True)],
                        'out_size': 1
                    },
                    '19': {
                        'type': 'CM_JJOralCare_PriceImpact',
                        'parameters': {'type': 'exp', 'above_count': 2},
                        'coefficients': [5],
                        'input_pins': [('inp', 6, True), ('17', 0, True),
                                       ('inp', 10, True), ('18', 0, True),
                                       ('inp', 1, True), ('8', 0, True),
                                       ('inp', 15, True)],
                        'out_size': 1
                    },
                    # Sum Lifts.
                    '20': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('2', 0, True),
                            ('4', 0, True),
                            ('6', 0, True),
                            ('9', 0, True),
                            ('11', 0, True),
                            ('13', 0, True),
                            ('16', 0, True),
                            ('19', 0, True),
                            ('inp', 14, True)
                        ],
                        'out_size': 1
                    },
                    '21': {
                        'type': 'CM_Sum',
                        'input_pins': [
                            ('20', 0, True),
                            ('const', 0, True)
                        ],
                        'out_size': 1
                    },
                    # EQ Volume
                    '22': {
                        'type': 'CM_Delay_Switch',
                        'parameters': {'delay': 1},
                        'input_pins': [('inp', 3, True), ('23', 0, False)],
                        'out_size': 1
                    },



                    '23': {
                        'type': 'CM_Multiply',
                        'input_pins': [('21', 0, True), ('22', 0, True)],
                        'out_size': 1
                    },
                    # Price Per EQ
                    '24': {
                        'type': 'CM_Divide',
                        'input_pins':[('inp', 6, True), ('inp', 7, True)],
                        'out_size': 1
                    },
                    # Sales Value
                    '25': {
                        'type': 'CM_Multiply',
                        'input_pins': [('23', 0, True), ('24', 0, True)],
                        'out_size': 1
                    },
                    # Sales Units
                    '26': {
                        'type': 'CM_Divide',
                        'input_pins': [('22', 0, True), ('inp', 7, True)],
                        'out_size': 1
                    }
                }
        }
    },



    {
        'name': 'country growth',
        'input_timescale': 'annual',
        'output_timescale': 'annual',
        'input_item': {'type': 3, 'meta_filter': ('Geography', 'Country')},
        'coefficients': [],
        'inputs': [
            {
                'meta': {'type': 0},
                'data': ['Population total', 'CPI', 'GDP PC']
            },
        ],
        'output': ['Population total', 'CPI', 'GDP PC'],
        'scheme': {
            'output': [('0', 0), ('1', 0), ('2', 0)],
            'constants': [-1],
            'modules': {
                '1': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 0, True)],
                    'out_size': 1
                },
                '2': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 1, True)],
                    'out_size': 1
                },
                '3': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 2, True)],
                    'out_size': 1
                },

            }
        }
    },


    {
        'name': 'country cagrs',
        'input_timescale': 'annual',
        'output_timescale': 'annual',
        'input_item': {'type': 3, 'meta_filter': ('Geography', 'Country')},
        'coefficients': [],
        'inputs': [
            {
                'meta': {'type': 0},
                'data': ['Population total', 'CPI', 'GDP PC']
            },
        ],
        'output': ['gr_Population total', 'gr_CPI', 'gr_GDP PC'],
        'scheme': {
            'output': [('0', 0), ('1', 0), ('2', 0)],
            'constants': [-1],
            'modules': {
                '1': {
                    'type': 'CM_CAGR',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 0, True)],
                    'out_size': 1
                },
                '2': {
                    'type': 'CM_CAGR',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 1, True)],
                    'out_size': 1
                },
                '3': {
                    'type': 'CM_CAGR',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 2, True)],
                    'out_size': 1
                }
            }
        }
    },


    {
        'name': 'category growth rates',
        'input_timescale': 'annual',
        'output_timescale': 'annual',
        'input_item': {'type': 3, 'meta_filter': ('Products', 'Category')},
        'coefficients': [],
        'inputs': [
            {
                'meta': {'type': 0},
                'data': [
                    'EQ Volume',
                    'Unit Volume',
                    'Price per EQ',
                    'Price per Unit',
                    'Unit Size',
                    'Distribution',
                    'Innovation TDP share',
                    'Premiumization',
                    'Media Spend',
                    'Avg % Discount',
                    'Avg % Promo Support',
                    'LTT'
                ]
            }
        ],
        'output': ['gr_EQ Volume', 'gr_Unit Volume', 'gr_Price per EQ',
                    'gr_Price per Unit', 'gr_Unit Size', 'gr_Distribution',
                    'gr_Innovation TDP share', 'gr_Premiumization',
                    'gr_Media Spend', 'gr_Avg % Discount', 'gr_Avg % Promo Support',
                    'gr_LTT'],
        'scheme': {
            'output': [('1', 0), ('2', 0), ('3', 0), ('4', 0), ('5', 0),
                       ('6', 0), ('7', 0), ('8', 0), ('9', 0), ('10', 0),
                        ('11', 0), ('12', 0)],
            'constants': [-1],
            'modules': {
                '1': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 0, True)],
                    'out_size': 1
                },
                '2': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 1, True)],
                    'out_size': 1
                },
                '3': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 2, True)],
                    'out_size': 1
                },
                '4': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 3, True)],
                    'out_size': 1
                },
                '5': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 4, True)],
                    'out_size': 1
                },
                '6': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 5, True)],
                    'out_size': 1
                },
                '7': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'rate'},
                    'input_pins': [('inp', 6, True)],
                    'out_size': 1
                },
                '8': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 7, True)],
                    'out_size': 1
                },
                '9': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'abs'},
                    'input_pins': [('inp', 8, True)],
                    'out_size': 1
                },
                '10': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'rate'},
                    'input_pins': [('inp', 9, True)],
                    'out_size': 1
                },
                '11': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'rate'},
                    'input_pins': [('inp', 10, True)],
                    'out_size': 1
                },
                '12': {
                    'type': 'CM_GrowthRate',
                    'parameters': {'delay': 1, 'type': 'rate'},
                    'input_pins': [('inp', 11, True)],
                    'out_size': 1
                }
            }
        }
    }

]