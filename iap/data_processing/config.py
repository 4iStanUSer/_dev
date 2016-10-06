from collections import OrderedDict

config = {
    'jj_oc_input_sales_data': {
        'func': 'jj_oc_data_proc',
        'date_func': 'date_year_month',
        'info': {'header_row': 2, 'data_row': 3},
        'meta_cols': OrderedDict({0: '', 1: '', 2: 'NewBrand', 3: ''}),
        'name_col': 4,
        'properties': {5: 'Metric'},
        'dates_cols': {
            'scale': 'monthly',
            'date_name_rows': [0, 2],
            'start_column': 6,
            'end_column': ''
        }
    },
    'jj_oc_input_trends': {
        'func': 'jj_oc_data_proc',
        'date_func': 'date_year',
        'info': {'header_row': 1, 'data_row': 2},
        'meta_cols': OrderedDict({0: ''}),
        'name_col': 1,
        'properties': {2: 'Facts', 3: '', 4: ''},
        'dates_cols': {
            'scale': 'years',
            'date_name_rows': [1],
            'start_column': 5,
            'end_column': ''
        }
    },
    'MyReport (Benadryl SI Other Accaunts)': {
        'func': 'jj_brand',
        'date_func': 'date_jj_1week',
        'info': 'N/A',
        'meta_cols': [
            {
                'Layer': 'Chanel',
                'Dimension_name': 'Chanel Distribution',
                'Name': '',
                'Order': 3
            },
            {
                'Layer': 'None',
                'Dimension_name': 'None',
                'Name': '', 'Order': 0
            },
            {
                'Layer': 'Nope',
                'Dimension_name': 'None2',
                'Name': '', 'Order': 0
            },
            {
                'Layer': 'Brand',
                'Dimension_name': 'Products',
                'Name': '', 'Order': 1
            },
            {
                'Layer': 'Segment',
                'Dimension_name': 'Products',
                'Name': '',
                'Order': 2
            }
         ],
        'name_col': 0,
        'properties': 'N/A',
        'dates_cols': {
            'scale': 'weekly',
            'date_name_rows': 'N/A',
            'start_column': 1,
            'end_column': ''
        },
        'mapping_rule': [
            {
                'in': OrderedDict({'Products': 'PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'ULTRA PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'DECORATED BNDG'}),
                'out': OrderedDict({'Products': 'Decorated'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'VALUE BNDG'}),
                'out': OrderedDict({'Products': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'REM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL SI'}),
                'out': OrderedDict({'Products': 'Benadryl SI'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL'}),
                'out': OrderedDict({'Products': 'Benadryl'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BAND-AID'}),
                'out': OrderedDict({'Products': 'Band-Aid'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walmart Total US TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Wal-mart'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Target Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Target'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'CVS Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'CSV'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walgreens Corp Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Walgreens'}),
                'rule': 'rename'
            }
        ]
    },
    'MyReport (Band-aid Other Accaunts)': {
        'func': 'jj_brand',
        'date_func': 'date_jj_1week',
        'info': 'N/A',
        'meta_cols': [
            {
                'Layer': 'Chanel',
                'Dimension_name': 'Chanel Distribution',
                'Name': '', 'Order': 3
            },
            {
                'Layer': 'None',
                'Dimension_name': 'None',
                'Name': '',
                'Order': 0
            },
            {
                'Layer': 'Brand',
                'Dimension_name': 'Products',
                'Name': '',
                'Order': 1
            },
            {
                'Layer': 'Segment',
                'Dimension_name': 'Products',
                'Name': '',
                'Order': 2
            }
        ],
        'name_col': 0,
        'properties': 'N/A',
        'dates_cols': {
            'scale': 'weekly',
            'date_name_rows': 'N/A',
            'start_column': 1,
            'end_column': ''
        },
        'mapping_rule': [
            {
                'in': OrderedDict({'Products': 'PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'ULTRA PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'DECORATED BNDG'}),
                'out': OrderedDict({'Products': 'Decorated'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'VALUE BNDG'}),
                'out': OrderedDict({'Products': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'REM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL SI'}),
                'out': OrderedDict({'Products': 'Benadryl SI'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL'}),
                'out': OrderedDict({'Products': 'Benadryl'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BAND-AID'}),
                'out': OrderedDict({'Products': 'Band-Aid'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walmart Total US TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Wal-mart'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Target Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Target'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'CVS Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'CSV'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walgreens Corp Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Walgreens'}),
                'rule': 'rename'
            }
        ]
    },
    'MyReport (Wallmart)': {
        'func': 'jj_brand',
        'date_func': 'date_jj_1week',
        'info': 'N/A',
        'meta_cols': [
            {
                'Layer': 'Chanel',
                'Dimension_name': 'Chanel Distribution',
                'Name': '',
                'Order': 3
            },
            {
                'Layer': 'Nope',
                'Dimension_name': 'NopeNope',
                'Name': '',
                'Order': 0
            },
            {
                'Layer': 'Brand',
                'Dimension_name': 'Products',
                'Name': '',
                'Order': 1
            },
            {
                'Layer': 'Segment',
                'Dimension_name': 'Products',
                'Name': '',
                'Order': 2
            }
        ],
        'name_col': 0,
        'properties': 'N/A',
        'dates_cols': {
            'scale': 'weekly',
            'date_name_rows': 'N/A',
            'start_column': 1,
            'end_column': ''
        },
        'mapping_rule': [
            {
                'in': OrderedDict({'Products': 'PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'ULTRA PREMIUM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'DECORATED BNDG'}),
                'out': OrderedDict({'Products': 'Decorated'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'VALUE BNDG'}),
                'out': OrderedDict({'Products': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'REM BNDG'}),
                'out': OrderedDict({'Products': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL SI'}),
                'out': OrderedDict({'Products': 'Benadryl SI'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BENADRYL'}),
                'out': OrderedDict({'Products': 'Benadryl'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Products': 'BAND-AID'}),
                'out': OrderedDict({'Products': 'Band-Aid'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walmart Total US TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Wal-mart'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Target Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Target'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'CVS Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'CSV'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Chanel Distribution': 'Walgreens Corp Total TA'}),
                'out': OrderedDict({'Chanel Distribution': 'Walgreens'}),
                'rule': 'rename'
            }
        ]
    },
    'JNJ_lean_media_Band-aid': {
        'func': 'jj_brand_media_spend',
        'date_func': 'date_monthly_excel_number',
        'info': 'N/A',
        'meta_cols': [
            {
                'Layer': 'Country',
                'Dimension_name': 'Geography',
                'Name': 'US'
            },
            {'Layer': 'Brand',
             'Dimension_name': 'Products',
             'Name': 'BAND-AID'
             }
        ],
        'name_col': 4,
        'properties': 'N/A',
        'dates_cols': {
            'scale': '4-4-5',
            'date_name_rows': 'N/A',
            'start_column': 5,
            'end_column': ''
        }
    },
    'JNJ_SALES_EXTRACT_FOR_4I_201603': {
        'func': 'jj_brand_extract',
        'date_func': 'date_yyyyww',
        'info': 'N/A',
        'meta_cols': [
            {
                'Layer': 'Products',
                'Dimension_name': 'Market',
                'Name': '',
                'Col_number': 4
            },
            {
                'Layer': 'Products',
                'Dimension_name': 'Segments',
                'Name': '',
                'Col_number': 7
            }
        ],
        'name_col': 'N/A',
        'properties': 'N/A',
        'dates_cols': {
            'scale': 'weekly',
            'date_col': 1
        },
        'data_cols': {
            (10, 'int'): '',
            (11, 'float'): '',
            (12, 'int'): '',
            (13, 'float'): '',
            (14, 'int'): '',
            (15, 'float'): ''
        },
        'mapping_rule': [
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND ADH BDGS OTHER'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND ADHESIVE PADS'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND ANTIBIOTIC BNDGES'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND BLISTER'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND FLEXIBLE FABRIC'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND SPORT STRIP'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND TOUGH STRIP'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND VARIETY'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND WATERBLOCK'}),
                'out': OrderedDict({'Segments': 'Premium'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND CLEAR'}),
                'out': OrderedDict({'Segments': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND PLASTIC'}),
                'out': OrderedDict({'Segments': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND SHEER'}),
                'out': OrderedDict({'Segments': 'Value'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BAND-AID BRAND DECORATED'}),
                'out': OrderedDict({'Segments': 'Deco'}),
                'rule': 'rename'
            },
            {
                'in': OrderedDict({'Segments': 'BENADRYL BASE ADULT'}),
                'out': OrderedDict({'Segments': 'Benadryl'}),
                'rule': 'rename'
            }
        ]
    },
    'jj_oral_care_sku_data': {
        'func': 'jj_oral_care_sku',
        'date_func': 'date_monthly_excel_number',
        'info': {'header_row': 0, 'data_row': 1},
        'meta_cols': [
            {
                'Layer': 'Geography',
                'Dimension_name': 'Region',
                'Name': '',
                'Col_number': 0
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 1
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 2
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 3
            }
        ],
        'name_col': 4,
        'map_names': {'Value Sales LC': 'Values_sales_lc'},
        'dates_info': {
            'scale': 'monthly',
            'start_column': 5,
            'end_column': ''
        }
    },
    'jj_oral_care_sku_data_media_spend': {
        'func': 'jj_oral_care_media_spend',
        'date_func': 'date_year_month',
        'info': {'header_row': 2, 'data_row': 3},
        'meta_cols': [
            {
                'Layer': 'Geography',
                'Dimension_name': 'Country',
                'Name': '',
                'Col_number': 0
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 1
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 2
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 3
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 4
            }
        ],
        'name_col': 5,
        'dates_info': {
            'scale': '4-4-5',
            'start_column': 6,
            'end_column': '',
            'dates_rows': [0, 2]
        }
    },
    'jj_oral_care_rgm_sales': {
        'func': 'jj_oral_care_rgm_sales',
        'date_func': 'date_year_month',
        'info': {'header_row': 11, 'data_row': 12},
        'meta_cols': [
            {
                'Layer': 'Geography',
                'Dimension_name': 'Country',
                'Name': '',
                'Col_number': 0
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 1
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 2
            },
            {
                'Layer': 'Products',
                'Dimension_name': '',
                'Name': '',
                'Col_number': 3
            }
        ],
        'name_col': 4,
        'dates_info': {
            'scale': 'monthly',
            'start_column': 5,
            'end_column': '',
            'dates_rows': [9, 11]
        }
    }
}
