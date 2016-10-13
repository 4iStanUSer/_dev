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
        },
        sales: {
            name: 'Sales',
            metric: '$',
            multiplier: 'MM',
            type: 'output',
        },
        volume: {
            name: 'Volume',
            metric: 'EQ',
            multiplier: 'Thousands',
            type: 'output'
        },
        price: {
            name: 'Price',
            metric: 'per EQ',
            multiplier: '$',
            type: 'output'
        }
    };

    private data = {
        annual: {
            sales: [
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
            volume: [
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
            ],
            price: [
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
            sales: [
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
            volume: [
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
            ],
            price: [
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
            sales: [
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
            volume: [
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
            ],
            price: [
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
        sales: [
            {'start': 2010, 'end': 2013, 'value': 0.25},
            {'start': 2010, 'end': 2012, 'value': 0.12},
            {'start': 2012, 'end': 2013, 'value': 0.13}
        ],
        volume: [
            {'start': 2010, 'end': 2013, 'value': 0.25},
            {'start': 2010, 'end': 2012, 'value': 0.10},
            {'start': 2012, 'end': 2013, 'value': 0.15}
        ],
        price: [
            {'start': 2010, 'end': 2013, 'value': 0.25},
            {'start': 2010, 'end': 2012, 'value': 0.22},
            {'start': 2012, 'end': 2013, 'value': 0.25}
        ]
    };

    private decomposition = [
        {
            start: '2010',
            end: '2013',
            sales: [
                {
                    name: '2010',
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
                    name: '2013'
                },
            ],
            volume: [
                {
                    name: '2010',
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
                    name: '2013'
                }
            ],
            price: [
                {
                    name: '2010',
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
                    name: '2013'
                }
            ]
        }
    ];

    constructor(private req: AjaxService) {
        this.recreateScales();
    }

    public getData_Waterfall(timelabelIds: Array<number>, variables: Array<string>) {
        let start = this.timelabels[timelabelIds[0]]['name'];
        let end = this.timelabels[timelabelIds[timelabelIds.length - 1]]['name'];
        let found = false;
        let i = 0;
        while (i < this.decomposition.length && !found) {
            if (
                this.decomposition[i]['start'].toString() == start
                && this.decomposition[i]['end'].toString() == end
            ) {
                found = true;
            } else {
                i++;
            }
        }
        console.log(123);
        if (found) {
            let waterfall = {
                'base_name': 'Decomposition',
                'variables': variables.map(function(variable){
                    let v = this.variables[variable];
                    return {
                        'name': v['name'],
                        'key': variable,
                        'metric': v['metric'],
                        'multiplier': v['multiplier']
                    };
                }, this),
                'start': this.decomposition[i]['start'],
                'end': this.decomposition[i]['end']
            };
            for (let j=0;j<variables.length;j++) {
                let v = variables[j];
                waterfall[v] = this.decomposition[i][v];
            }
            return waterfall;
        } else {
            // TODO Procedure for requesting more decomposition
        }
    }

    public getData_Bar(timelabelIds: Array<number>, variables: Array<string>) {
        let variable: string = null;
        let timescale: string = this.timelabels[timelabelIds[0]]['timescale'];
        let bars: Array<Object> = [];

        let timelabelsForCagrs = this.getTwoCagrPeriods(timelabelIds);

        for (let i = 0; i < variables.length; i++) {
            variable = variables[i];
            // TODO Check existing
            if (this.data[timescale] && this.data[timescale][variable]) {
                let data = this.data[timescale][variable]
                    .filter(function (el) {
                        return (timelabelIds.indexOf(el['timelabels_index']) != -1)
                            ? true : false;
                    })
                    .map(function (el) {
                        return {
                            'name': this.timelabels[el['timelabels_index']]['name'],
                            'value': el['value']
                        }
                    }, this);
                let cagrs = timelabelsForCagrs.map(function(el){
                    return this.getCagrsForPeriod(variable,
                        el['start'], el['end']);
                }, this);

                bars.push({
                    'name': variable,
                    'variable': this.variables[variable],
                    'cagrs': cagrs,
                    'data': data
                });
            }
        }
        return bars;
    }

    public getData_Donut(timelabelIds: Array<number>, variables: Array<string>) {
        let variable: string = null;
        let donuts = [];

        let timelabelsForCagrs = this.getTwoCagrPeriods([
            timelabelIds[0],
            timelabelIds[timelabelIds.length - 1]
        ]); // TODO Review. Only one element!

        for (let i = 0; i < variables.length; i++) {
            variable = variables[i];
            let cagr = this.getCagrsForPeriod(variable,
                timelabelsForCagrs[0]['start'],
                timelabelsForCagrs[0]['end']);

            donuts.push({
                'name': this.variables[variable]['name'],
                'value': cagr['value'] * 100 // !!!
            });
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

    ////////////////////////////////
    public getTwoCagrPeriods(timelabelIds: Array<string|number>) {
        let timelabels = [];
        if (timelabelIds.length < 3) {
            timelabels = [
                {
                    start: this.timelabels[timelabelIds[0]]['name'],
                    end: this.timelabels[timelabelIds[timelabelIds.length - 1]]['name']
                }
            ];
        } else {
            let _middleId = timelabelIds[Math.floor(timelabelIds.length / 2)];
            timelabels = [
                {
                    start: this.timelabels[timelabelIds[0]]['name'],
                    end: this.timelabels[_middleId]['name']
                },
                {
                    start: this.timelabels[_middleId]['name'],
                    end: this.timelabels[timelabelIds[timelabelIds.length - 1]]['name']
                }
            ];
        }
        return timelabels;
    }

    public getCagrsForPeriod(variable: string, start: string|number,
                             end: string|number) {
        start = start.toString();
        end = end.toString();
        for (let i = 0; i < this.cagrs[variable].length; i++) {
            if (this.cagrs[variable][i]['start'].toString() == start
                && this.cagrs[variable][i]['end'].toString() == end) {
                return this.cagrs[variable][i];
            }
        }
    }

    public getVarsByType(type: string): Array<string> {
        let vars = [];
        for (let v in this.variables) {
            if (this.variables[v]['type'] == type) {
                vars.push(v);
            }
        }
        return vars;
    }

    public getShortTimeLablesForOutput(timescale: string): Array<number> {
        let longLables = this.getLongTimeLablesForOutput(timescale);
        if (longLables.length < 3) {
            return longLables;
        } else {
            return [
                longLables[0],
                longLables[Math.floor(longLables.length / 2)],
                longLables[longLables.length - 1],
            ];
        }
    }

    public getLongTimeLablesForOutput(timescale: string): Array<number> {
        // TODO Review sorting...
        let vars = this.getVarsByType('output');
        let timelables = [];
        if (vars) {
            timelables = this.data[timescale][vars[0]].map(function (el) {
                return el['timelabels_index'];
            });
        }
        return timelables;
    }

    ////////////////////////////////


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
