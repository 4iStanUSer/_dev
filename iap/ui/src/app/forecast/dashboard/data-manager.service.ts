import {Injectable} from '@angular/core';
// import * as _ from 'lodash';
import {AjaxService} from "./../../common/service/ajax.service";

@Injectable()
export class DataManagerService {

    public hTableData: Object = {};


    private widgetsConfig = {
        'vertical_table': {},
        'horizontal_table': {},
        'waterfall_chart': {},
        'donut_chart': {},
        'bar_chart': {}
    };

    private scales: Array<string> = [];

    // private scalesTree: Array<Object> = [];

    private hierarchy = [];

    private timelabels = [
        {
            name: 2010,
            timescale: 'annual',
            parent_index: null
        },
        {
            name: 2011,
            timescale: 'annual',
            parent_index: null
        },
        {
            name: 2012,
            timescale: 'annual',
            parent_index: null
        },
        {
            name: 2013,
            timescale: 'annual',
            parent_index: null
        },

        //

        {
            name: 'Q1',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            name: 'Q2',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            name: 'Q3',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            name: 'Q4',
            timescale: 'quarterly',
            parent_index: 0
        },

        {
            name: 'Q1',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            name: 'Q2',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            name: 'Q3',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            name: 'Q4',
            timescale: 'quarterly',
            parent_index: 1
        },

        {
            name: 'Q1',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            name: 'Q2',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            name: 'Q3',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            name: 'Q4',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            name: 'Q1',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            name: 'Q2',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            name: 'Q3',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            name: 'Q4',
            timescale: 'quarterly',
            parent_index: 3
        },

        //

        {
            name: 'Jan',
            timescale: 'monthly',
            parent_index: 4
        },
        {
            name: 'Feb',
            timescale: 'monthly',
            parent_index: 4
        },
        {
            name: 'Mar',
            timescale: 'monthly',
            parent_index: 4
        },

        {
            name: 'Jan',
            timescale: 'monthly',
            parent_index: 8
        },
        {
            name: 'Feb',
            timescale: 'monthly',
            parent_index: 8
        },
        {
            name: 'Mar',
            timescale: 'monthly',
            parent_index: 8
        },
    ];

    private variables = {
        CPI: {
            name: 'CPI',
            metric: 'index',
            multiplier: null,
            type: 'driver', // | 'output',
            driver_type: 'economic' // | null
        },
        GDP: {
            name: 'GDP',
            metric: 'index',
            multiplier: null,
            type: 'driver',
            driver_type: 'economic'
        }
    };

    private data = {
        annual: {
            CPI: [
                {
                    'timelabels_index': 0,
                    'value': 0,
                    'gr': 15,
                    // 'color',
                    // 'isEditable',
                    // 'format'
                },
                {
                    'timelabels_index': 1,
                    'value': 1,
                    'gr': 15
                },
                {
                    'timelabels_index': 2,
                    'value': 2,
                    'gr': 15
                },
                {
                    'timelabels_index': 3,
                    'value': 3,
                    'gr': 15
                }
            ],
            GDP: [
                {
                    'timelabels_index': 0,
                    'value': 4,
                    'gr': 15
                },
                {
                    'timelabels_index': 1,
                    'value': 5,
                    'gr': 15
                },
                {
                    'timelabels_index': 2,
                    'value': 6,
                    'gr': 15
                },
                {
                    'timelabels_index': 3,
                    'value': 7,
                    'gr': 15
                }
            ]
        },
        quarterly: {
            CPI: [
                {
                    'timelabels_index': 4,
                    'value': 8,
                    'gr': 15
                },
                {
                    'timelabels_index': 5,
                    'value': 9,
                    'gr': 15
                },
                {
                    'timelabels_index': 6,
                    'value': 10,
                    'gr': 15
                },
                {
                    'timelabels_index': 7,
                    'value': 11,
                    'gr': 15
                },
            ],
            GDP: [
                {
                    'timelabels_index': 4,
                    'value': 12,
                    'gr': 15
                },
                {
                    'timelabels_index': 5,
                    'value': 13,
                    'gr': 15
                },
                {
                    'timelabels_index': 6,
                    'value': 14,
                    'gr': 15
                },
                {
                    'timelabels_index': 7,
                    'value': 15,
                    'gr': 15
                },
            ]
        },
        monthly: {
            CPI: [
                {
                    'timelabels_index': 20,
                    'value': 16,
                    'gr': 15
                },
                {
                    'timelabels_index': 21,
                    'value': 17,
                    'gr': 15
                },
                {
                    'timelabels_index': 22,
                    'value': 18,
                    'gr': 15
                },
                {
                    'timelabels_index': 23,
                    'value': 19,
                    'gr': 15
                },
                {
                    'timelabels_index': 24,
                    'value': 20,
                    'gr': 15
                },
                {
                    'timelabels_index': 25,
                    'value': 21,
                    'gr': 15
                }
            ],
            GDP: [
                {
                    'timelabels_index': 20,
                    'value': 22,
                    'gr': 15
                },
                {
                    'timelabels_index': 21,
                    'value': 23,
                    'gr': 15
                },
                {
                    'timelabels_index': 22,
                    'value': 24,
                    'gr': 15
                },
                {
                    'timelabels_index': 23,
                    'value': 25,
                    'gr': 15
                },
                {
                    'timelabels_index': 24,
                    'value': 26,
                    'gr': 15
                },
                {
                    'timelabels_index': 25,
                    'value': 27,
                    'gr': 15
                }
            ]
        }
    };

    private cagrs = {
        CPI: [
            {'start': 2013, 'end': 2016, 'value': 0.12},
            {'start': 2016, 'end': 2020, 'value': 0.13}
        ],
        GDP: [
            {'start': 2013, 'end': 2016, 'value': 0.10},
            {'start': 2016, 'end': 2020, 'value': 0.11}
        ]
    };

    private decomposition = [
        {
            start: '2016',
            end: '2020',
            values: [
                {
                    name: '2016',
                    value: 100,
                    growth: 100,
                    children: null
                },
                {
                    name: 'Economic',
                    value: 2.15,
                    growth: 5,
                    children: null
                },
                {
                    name: 'Inflation',
                    value: 3.15,
                    growth: 4,
                    children: null
                },
                {
                    name: 'Pricing',
                    value: 4.15,
                    growth: 2,
                    children: null
                },
                {
                    name: '2020'
                },
            ],
            volume: [
                {
                    name: '2016',
                    value: 15,
                    growth: 15,
                    children: null
                },
                {
                    name: 'Inflation',
                    value: 3.15,
                    growth: 2,
                    children: null
                },
                {
                    name: 'Pricing',
                    value: 4.15,
                    growth: 2,
                    children: null
                },
                {
                    name: '2020'
                }
            ]
        }
    ];

    constructor(private req: AjaxService) {
        this.recreateScales();
    }

    public getData_Waterfall(start: number|string, end: number|string) {
        let found = false;
        let i = 0;
        while (i < this.decomposition.length && !found) {
            if (
                this.decomposition[i]['start'] == start
                && this.decomposition[i]['end'] == end
            ) {
                found = true;
            } else {
                i++;
            }
        }
        if (found) {
            return {
                // 'modes': [
                //     {
                //         'key': 'growth',
                //         'name': 'Growth rate'
                //     },
                //     {
                //         'key': 'value',
                //         'name': 'Absolute'
                //     }
                // ],
                'variables': [
                    {
                        'name': 'Value',
                        'key': 'values',
                        'metric': 'piece'
                    },
                    {
                        'name': 'Volume',
                        'key': 'volume',
                        'metric': 'USD'
                    }
                ],
                'base_name': 'Decomposition',
                'start': this.decomposition[i]['start'],
                'end': this.decomposition[i]['end'],
                'values': this.decomposition[i]['values'],
                'volume': this.decomposition[i]['volume']
            }
        } else {
            // TODO Procedure for requesting more decomposition
        }
    }

    public getData_Bar(timescale: string, variables: Array<string>) {
        let bars: Array<Object> = [];
        let variable: string = null;
        for (let i = 0; i < variables.length; i++) {
            variable = variables[i];
            // TODO Check existing
            if (this.data[timescale] && this.data[timescale][variable]) {
                bars.push({
                    'name': variable,
                    'data': this.data[timescale][variable].map(function (el) {
                        return {
                            'name': this.timelabels[el['timelabels_index']]['name'].toString(),
                            'value': el['value']
                        };
                    }, this)
                });
            }
        }
        return bars;
    }

    public getData_Donut(start: number|string, end: number|string) {
        let vars = ['CPI', 'GDP'];
        let donuts = [];
        for (let i = 0; i < vars.length; i++) {
            if (this.cagrs[vars[i]]) {
                let j = 0;
                let found = false;
                while (j < this.cagrs[vars[i]].length && found === false) {
                    if (
                        this.cagrs[vars[i]][j]['start'] == start
                        &&
                        this.cagrs[vars[i]][j]['end'] == end
                    ) {
                        donuts.push({
                            'name': vars[i],
                            'value': this.cagrs[vars[i]][j]['value'] * 100 // !!!
                        });
                        found = true;
                    }
                    j++;
                }
                if (!found) {
                    // TODO Procedure for requesting more cagrs
                }
            } else {
                // TODO Procedure for requesting more cagrs
            }
        }
        return donuts;
    }

    public getData_VTable() {
        return {
            'variables': this.variables,
            'data': this.data,
            'timelabels': this.timelabels,
            'scales_order': this.scales, // ['annual', 'quarterly', 'monthly']
            'config': {
                'head': {
                    'horizontal_order': ['CPI', 'GDP'],
                    'vertical_order': [
                        {
                            'key': 'name',
                            'label': 'Name'
                        },
                        {
                            'key': 'metric',
                            'label': 'Metric'
                        }
                    ]
                }
            }
        };
    }

    public getData_HTable() {
    }




    private digInitialData() {
        // TODO Implement method getInitialData()
    }

    private digMoreDecomposition() {
        // TODO Implement method digMoreDecomposition()
    }

    private recreateScales(): void {
        this.scales = [];

        let pIndex: number = null;
        let ts: string = null;
        let relations: { [s: string]: string; } = {}; // {child: parent}

        for (let i = 0; i < this.timelabels.length; i++) {
            pIndex = this.timelabels[i]['parent_index'];
            ts = this.timelabels[i]['timescale'];

            if (!('children' in this.timelabels[i])) {
                this.timelabels[i]['children'] = [];
            }

            if (pIndex !== null) {
                if (!this.timelabels[pIndex]) {
                    console.error('Not found such index ' + pIndex);
                    break;
                }
                if (!('children' in this.timelabels[pIndex])) {
                    this.timelabels[pIndex]['children'] = [];
                }
                this.timelabels[pIndex]['children'].push(i);
            }
            if (!(ts in relations)) {
                if (pIndex !== null) {
                    relations[ts] = this.timelabels[pIndex]['timescale'];
                } else {
                    relations[ts] = null;
                }
            }
        }

        let parentTS = DataManagerService._findKey(relations, null);
        if (parentTS) {
            this.scales.push(parentTS);
            let relLength = Object.keys(relations).length;
            let childTS = null;
            while (relLength != this.scales.length) {
                childTS = DataManagerService._findKey(relations, parentTS);
                if (childTS) {
                    this.scales.push(childTS);
                    parentTS = childTS;
                } else {
                    console.error('Something wrong: have no such value');
                    break;
                }
            }
        }
    }

    public static _findKey(obj: Object, value: any): string {
        for (var prop in obj) {
            if (obj.hasOwnProperty(prop)) {
                if (obj[prop] === value)
                    return prop;
            }
        }
    }
}
