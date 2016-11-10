import {ButtonDataInput} from "../../../common/cmp/buttons-group/buttons-group.component";

/**
 * Buttons for Value/GrowthRate ButtonsGroup inside forecast section
 * @type {{id: string; name: string; selected: boolean}[]}
 */
export const forecastValueRateData: Array<ButtonDataInput> = [
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
