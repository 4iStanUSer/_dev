import {ButtonsGroupDataInput} from "./../../common/cmp/buttons-group/buttons-group.component";
import {TableWidgetData} from "./../../common/cmp/table-widget/table-widget.component";

/**
 * Buttons for Value/GrowthRate ButtonsGroup inside forecast section
 * @type {{id: string; name: string; selected: boolean}[]}
 */
export const forecastValueRateData: ButtonsGroupDataInput = [
    {
        id: 'absolute',
        name: 'Value',
        selected: true
    },
    {
        id: 'rate',
        name: 'Growth rate',
        selected: false
    }
];

export const defaultState = {
    'forecast_timescale': 'annual', // annual|quarterly|monthly
    'forecast_absolute_rate': 'absolute', // absolute|rate
    'forecast_collapse_expand': 'collapse', // collapse|expand
    'forecast_active_tab': 'all', // all|(name of variable)
    'forecast_tab': 'all', // all|(or name of variable)
    'decomp_value_volume_price': 'Value', // value|volume|price (name of type)

    'd_summary_table_collapsed_expanded': 'expanded', // collapsed|expanded

    'd_details_table_collapsed_expanded': 'expanded', // collapsed|expanded

    'd_details_selected_megadriver': null, // null(get first)|mega driver key
};

export const dashboardConfig = {
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
};





/*=====================TEMP======================*/
export const selectorsConfigTEMP = {
    selectors: {
        brand: {
            name: 'Brand',
            placeholder: 'brand',
            multiple: true, // false|true,
            type: 'flat', // flat | hierarchical | region
            icon: '',
            disabled: false,
        },
        category: {
            name: 'Category',
            placeholder: 'category',
            multiple: true,
            type: 'hierarchical', // flat | hierarchical | region
            icon: '',
            disabled: false,
        },
        // channel: {
        //     name: 'Channel',
        //     placeholder: 'channel',
        //     multiple: true,
        //     type: 'flat', // flat | hierarchical | region
        //     icon: ''
        // },
    },
    order: ['brand', 'category'] //, 'channel'
};
export const selectorsDataTEMP = {
    brand: {
        data: [
            {
                name: 'Puma',
                id: 'puma',
                parent_id: null
            },
            {
                name: 'Nike',
                id: 'nike',
                parent_id: null
            },
            {
                name: 'Adidas',
                id: 'adidas',
                parent_id: null
            }
        ],
        selected: ['puma', 'adidas']
    },
    category: {
        data: [
            {
                name: 'Puma',
                id: 'puma',
                parent_id: null
            },
            {
                name: 'Nike',
                id: 'nike',
                parent_id: null
            },
            {
                name: 'Adidas',
                id: 'adidas',
                parent_id: null
            },
            {
                name: 'Puma Black',
                id: 'puma_black',
                parent_id: 'puma'
            },
            {
                name: 'Nike Black',
                id: 'nike_black',
                parent_id: 'nike'
            },
            {
                name: 'Adidas Black',
                id: 'adidas_black',
                parent_id: 'adidas'
            },
        ],
        selected: ['adidas']
    }
};



export const vertTableTEMP: TableWidgetData = {
    selected_row_id: 'three',
    appendix: ['Driver', 'Metric'],
    rows: [
        {
            id: 'one',
            parent_id: null,
            meta:[{name: 'One'}]
        },
        {
            id: 'two',
            parent_id: null,
            meta:[{name: 'Two'}]
        },
        {
            id: 'three',
            parent_id: null,
            meta:[{name: 'Three'}]
        },
            {
                id: 'one-one',
                meta:[{name: 'One-One'}],
                parent_id: 'one',
            },
            {
                id: 'one-two',
                meta:[{name: 'One-Two'}],
                parent_id: 'one',
            },
            {
                id: 'one-three',
                meta:[{name: 'One-Three'}],
                parent_id: 'one',
            },

            {
                id: 'two-one',
                meta:[{name: 'Two-One'}],
                parent_id: 'two',
            },
            {
                id: 'two-two',
                meta:[{name: 'Two-Two'}],
                parent_id: 'two',
            },
            {
                id: 'two-three',
                meta:[{name: 'Two-Three'}],
                parent_id: 'two',
            },

                {
                    id: 'one-one-one',
                    meta:[{name: 'One-One-One'}],
                    parent_id: 'one-one',
                },
                {
                    id: 'one-one-two',
                    meta:[{name: 'One-One-Two'}],
                    parent_id: 'one-one',
                },
                {
                    id: 'one-one-three',
                    meta:[{name: 'One-One-Three'}],
                    parent_id: 'one-one',
                },
    ],
    cols: [
        {
            id: 'driver-1',
            parent_id: null,
            meta:[{name: 'driver-1'}, {name: 'metric-1'}]
        },
        {
            id: 'driver-2',
            parent_id: null,
            meta:[{name: 'driver-2'}, {name: 'metric-2'}]
        },
        {
            id: 'driver-3',
            parent_id: null,
            meta:[{name: 'driver-3'}, {name: 'metric-3'}]
        },
        {
            id: 'driver-4',
            parent_id: null,
            meta:[{name: 'driver-4'}, {name: 'metric-4'}]
        },
    ],
    values: {
        'one': {
            'driver-1': 10,
            'driver-2': 20,
            'driver-3': 30,
            'driver-4': 40,
        },
        'two': {
            'driver-1': 10,
            'driver-2': 20,
            'driver-3': 30,
            'driver-4': 40,
        },
        'three': {
            'driver-1': 10,
            'driver-2': 20,
            'driver-3': 30,
            'driver-4': 40,
        },
    }
};
