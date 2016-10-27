import {Injectable} from '@angular/core';
// import * as _ from 'lodash';
import {AjaxService} from "./../../common/service/ajax.service";

interface Cagr {
    start: string;
    end: string;
    value: number;
}
export interface Period {
    start: string;
    end: string;
}

@Injectable()
export class DataManagerService {

    // public hTableData: Object = {};
    // private widgetsConfig = {
    //     'vertical_table': {},
    //     'horizontal_table': {},
    //     'waterfall_chart': {},
    //     'donut_chart': {},
    //     'bar_chart': {}
    // };

    private scales: Array<string> = [];

    private timelabels = [];
    private variables = {};
    private data = {};
    private cagrs = {};

    private cagrPeriods: Array<{start: string, end: string}> = [];
    private timelabelsMap: {[timeLabel: string]: number} = {};


    ///////////////////////////////////
    public timelabelsTEST = [
        {
            full_name: '2010',
            short_name: '2010',
            timescale: 'annual',
            parent_index: null
        },
        {
            full_name: '2011',
            short_name: '2011',
            timescale: 'annual',
            parent_index: null
        },
        {
            full_name: '2012',
            short_name: '2012',
            timescale: 'annual',
            parent_index: null
        },
        {
            full_name: '2013',
            short_name: '2013',
            timescale: 'annual',
            parent_index: null
        },

        //

        {
            full_name: 'Q1 2010',
            short_name: 'Q1',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            full_name: 'Q2 2010',
            short_name: 'Q2',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            full_name: 'Q3 2010',
            short_name: 'Q3',
            timescale: 'quarterly',
            parent_index: 0
        },
        {
            full_name: 'Q4 2010',
            short_name: 'Q4',
            timescale: 'quarterly',
            parent_index: 0
        },

        {
            full_name: 'Q1 2011',
            short_name: 'Q1',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            full_name: 'Q2 2011',
            short_name: 'Q2',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            full_name: 'Q3 2011',
            short_name: 'Q3',
            timescale: 'quarterly',
            parent_index: 1
        },
        {
            full_name: 'Q4 2011',
            short_name: 'Q4',
            timescale: 'quarterly',
            parent_index: 1
        },

        {
            full_name: 'Q1 2012',
            short_name: 'Q1',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            full_name: 'Q2 2012',
            short_name: 'Q2',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            full_name: 'Q3 2012',
            short_name: 'Q3',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            full_name: 'Q4 2012',
            short_name: 'Q4',
            timescale: 'quarterly',
            parent_index: 2
        },
        {
            full_name: 'Q1 2013',
            short_name: 'Q1',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            full_name: 'Q2 2013',
            short_name: 'Q2',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            full_name: 'Q3 2013',
            short_name: 'Q3',
            timescale: 'quarterly',
            parent_index: 3
        },
        {
            full_name: 'Q4 2013',
            short_name: 'Q4',
            timescale: 'quarterly',
            parent_index: 3
        },

        //

        {
            full_name: 'Jan Q1 10',
            short_name: 'Jan',
            timescale: 'monthly',
            parent_index: 4
        },
        {
            full_name: 'Feb Q1 10',
            short_name: 'Feb',
            timescale: 'monthly',
            parent_index: 4
        },
        {
            full_name: 'Mar Q1 10',
            short_name: 'Mar',
            timescale: 'monthly',
            parent_index: 4
        },

        {
            full_name: 'Jan Q1 11',
            short_name: 'Jan',
            timescale: 'monthly',
            parent_index: 8
        },
        {
            full_name: 'Feb Q1 11',
            short_name: 'Feb',
            timescale: 'monthly',
            parent_index: 8
        },
        {
            full_name: 'Mar Q1 11',
            short_name: 'Mar',
            timescale: 'monthly',
            parent_index: 8
        },
    ];
    //
    // private variables = {
    //     CPI: {
    //         name: 'CPI',
    //         metric: 'index',
    //         multiplier: null,
    //         type: 'driver', // | 'output',
    //         driver_type: 'economic' // | null
    //     },
    //     GDP: {
    //         name: 'GDP',
    //         metric: 'index',
    //         multiplier: null,
    //         type: 'driver',
    //         driver_type: 'economic'
    //     },
    //     sales: {
    //         name: 'Sales',
    //         metric: '$',
    //         multiplier: 'MM',
    //         type: 'output',
    //     },
    //     volume: {
    //         name: 'Volume',
    //         metric: 'EQ',
    //         multiplier: 'Thousands',
    //         type: 'output'
    //     },
    //     price: {
    //         name: 'Price',
    //         metric: 'per EQ',
    //         multiplier: '$',
    //         type: 'output'
    //     }
    // };
    //
    // private data = {
    //     annual: {
    //         sales: [
    //             {
    //                 'timelabels_index': 0,
    //                 'value': 0,
    //                 'gr': 15,
    //                 // 'color',
    //                 // 'isEditable',
    //                 // 'format'
    //             },
    //             {
    //                 'timelabels_index': 1,
    //                 'value': 1,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 2,
    //                 'value': 2,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 3,
    //                 'value': 3,
    //                 'gr': 15
    //             }
    //         ],
    //         volume: [
    //             {
    //                 'timelabels_index': 0,
    //                 'value': 4,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 1,
    //                 'value': 5,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 2,
    //                 'value': 6,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 3,
    //                 'value': 7,
    //                 'gr': 15
    //             }
    //         ],
    //         price: [
    //             {
    //                 'timelabels_index': 0,
    //                 'value': 4,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 1,
    //                 'value': 5,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 2,
    //                 'value': 6,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 3,
    //                 'value': 7,
    //                 'gr': 15
    //             }
    //         ]
    //     },
    //     quarterly: {
    //         sales: [
    //             {
    //                 'timelabels_index': 4,
    //                 'value': 8,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 5,
    //                 'value': 9,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 6,
    //                 'value': 10,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 7,
    //                 'value': 11,
    //                 'gr': 15
    //             },
    //         ],
    //         volume: [
    //             {
    //                 'timelabels_index': 4,
    //                 'value': 12,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 5,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 6,
    //                 'value': 14,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 7,
    //                 'value': 15,
    //                 'gr': 15
    //             },
    //         ],
    //         price: [
    //             {
    //                 'timelabels_index': 4,
    //                 'value': 12,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 5,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 6,
    //                 'value': 14,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 7,
    //                 'value': 15,
    //                 'gr': 15
    //             },
    //         ]
    //     },
    //     monthly: {
    //         sales: [
    //             {
    //                 'timelabels_index': 20,
    //                 'value': 16,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 21,
    //                 'value': 17,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 22,
    //                 'value': 18,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 23,
    //                 'value': 19,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 24,
    //                 'value': 20,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 25,
    //                 'value': 21,
    //                 'gr': 15
    //             }
    //         ],
    //         volume: [
    //             {
    //                 'timelabels_index': 20,
    //                 'value': 22,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 21,
    //                 'value': 23,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 22,
    //                 'value': 24,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 23,
    //                 'value': 25,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 24,
    //                 'value': 26,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 25,
    //                 'value': 27,
    //                 'gr': 15
    //             }
    //         ],
    //         price: [
    //             {
    //                 'timelabels_index': 20,
    //                 'value': 22,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 21,
    //                 'value': 23,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 22,
    //                 'value': 24,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 23,
    //                 'value': 25,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 24,
    //                 'value': 26,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 25,
    //                 'value': 27,
    //                 'gr': 15
    //             }
    //         ]
    //     }
    // };
    //
    // private cagrs = {
    //     sales: [
    //         {'start': 2010, 'end': 2013, 'value': 0.25},
    //         {'start': 2010, 'end': 2012, 'value': 0.12},
    //         {'start': 2012, 'end': 2013, 'value': 0.13}
    //     ],
    //     volume: [
    //         {'start': 2010, 'end': 2013, 'value': 0.25},
    //         {'start': 2010, 'end': 2012, 'value': 0.10},
    //         {'start': 2012, 'end': 2013, 'value': 0.15}
    //     ],
    //     price: [
    //         {'start': 2010, 'end': 2013, 'value': 0.25},
    //         {'start': 2010, 'end': 2012, 'value': 0.22},
    //         {'start': 2012, 'end': 2013, 'value': 0.25}
    //     ]
    // };

    private decomposition = [
        {
            start: '2015',
            end: '2018',
            vars: [
                {
                    key: 'sales',
                    name: 'Sales',
                    metric: '$',
                    multiplier: 'MM',
                    values: [
                        {
                            name: '2015',
                            impact_abs: 100,
                            impact_rate: 100,
                            change_abs: null,
                            change_rate: null,
                            children: null
                        },
                        {
                            name: 'Economic',
                            impact_abs: 5,
                            impact_rate: 2.15,
                            change_abs: 10,
                            change_rate: 15,
                            children: null
                        },
                        {
                            name: 'Inflation',
                            impact_abs: 4,
                            impact_rate: 3.15,
                            change_abs: 12,
                            change_rate: 10,
                            children: null
                        },
                        {
                            name: 'Pricing',
                            impact_abs: 4.15,
                            impact_rate: 2,
                            change_abs: 22,
                            change_rate: 8,
                            children: null
                        },
                        {
                            name: '2018',
                            impact_abs: 4.15,
                            impact_rate: 2,
                            change_abs: null,
                            change_rate: null,
                            children: null
                        }
                    ]
                },
                {
                    key: 'volume',
                    name: 'Volume',
                    metric: 'EQ',
                    multiplier: 'Thousands',
                    values: [
                        {
                            name: '2015',
                            impact_abs: 100,
                            impact_rate: 100,
                            change_abs: null,
                            change_rate: null,
                            children: null
                        },
                        {
                            name: 'Inflation',
                            impact_abs: 4,
                            impact_rate: 3.15,
                            change_abs: 15,
                            change_rate: 10,
                            children: null
                        },
                        {
                            name: 'Pricing',
                            impact_abs: 4.15,
                            impact_rate: 2,
                            change_abs: 18,
                            change_rate: 8,
                            children: null
                        },
                        {
                            name: '2018',
                            impact_abs: 4.15,
                            impact_rate: 2,
                            change_abs: null,
                            change_rate: null,
                            children: null
                        }
                    ]
                },
            ]
        }
    ];

    constructor(private req: AjaxService) {
    }

    public init() {
        let resp = this.req.get({
            'url': '/forecast/get_dashboard_data',
            'data': {
                'entity_id': 2
            }
        });
        resp.subscribe((d)=> {
            this.timelabels = d['timelabels'];
            this.data = d['data'];
            this.cagrs = d['cagrs'];
            this.variables = d['variables'];

            // for (let i = 0; i < d['variables'].length; i++) { // TODO Remove
            //     this.variables[d['variables'][i]['name']] = d['variables'][i];
            // }

            // for filling cagr periods
            let cKeys: Array<string> = Object.keys(this.cagrs);
            if (cKeys.length) {
                for (let i = 0; i < this.cagrs[cKeys[0]].length; i++) {
                    let cagr = this.cagrs[cKeys[0]][i];
                    let exist = false;
                    for (let j = 0; j < this.cagrPeriods.length; j++) {
                        if (this.cagrPeriods[j]['start']
                            == cagr['start'].toString()
                            && this.cagrPeriods[j]['end']
                            == cagr['end'].toString()) {
                            exist = true;
                            break;
                        }
                    }
                    if (!exist) {
                        this.cagrPeriods.push({
                            'start': cagr['start'].toString(),
                            'end': cagr['end'].toString()
                        });
                    }
                }
            }

            // Fill timelabelsMap -> {timeLabel: timelabelIndex}
            for (let i = 0; i < this.timelabels.length; i++) {
                this.timelabelsMap[this.timelabels[i]['full_name']] = i;
            }

            this.recreateScales();
        });
        return resp;
    }

    public getData_Decomposition(p: Period) {
        if (!p || !p['start'] || !p['end']) {
            return null;
        }
        let start = p['start'].toString();
        let end = p['end'].toString();
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

        if (found) {
            let waterfall = {
                'base_name': 'Decomposition',
                'start': this.decomposition[i]['start'],
                'end': this.decomposition[i]['end'],
                'vars': this.decomposition[i]['vars'].map(function (v) {
                    return {
                        'name': v['name'],
                        'key': v['key'],
                        'metric': v['metric'],
                        'multiplier': v['multiplier'],
                        'values': v['values']
                    };
                }, this) // === this.decomposition[i]['vars']

            };
            return waterfall;
        } else {
            // TODO Procedure for requesting more decomposition
        }
    }

    /**
     *
     * @param period: {start: string, end: string}
     * @param variables Array<string>
     * @param mode: 'preview'|'full'
     * @returns {Array<Object>}
     */
    public getData_Bar(period: Period, variables: Array<string>,
                       mode: string): Array<Object> {
        if (!period
            || !period['start']
            || !period['end']
            || this.getTimelabelIndex(period['start']) === null
            || this.getTimelabelIndex(period['end']) === null
        ) {
            return null;
        }

        let startIndex = this.getTimelabelIndex(period['start']);
        let endIndex = this.getTimelabelIndex(period['end']);

        let bars: Array<Object> = [];
        let variable: string = null;
        let timescale: string = this.timelabels[startIndex]['timescale'];

        // Get all timelabels Ids for this timescale
        let timelabelIds = [];
        for (let i = startIndex; i <= endIndex; i++) {
            if (this.timelabels[i]['timescale'] == timescale) {
                timelabelIds.push(i);
            }
        }
        // Limit count of timelabels for preview mode
        if (mode == 'preview' && timelabelIds.length > 3) {
            timelabelIds = [
                timelabelIds[0],
                timelabelIds[Math.floor((timelabelIds.length - 1) / 2)],
                timelabelIds[timelabelIds.length - 1]
            ];
        }

        // Fill the timelabelsForCagrs
        let timelabelsForCagrs = [];
        if (timelabelIds.length >= 3) {
            let _middleId = timelabelIds[Math.floor(
                (timelabelIds.length - 1) / 2)];
            timelabelsForCagrs = [
                {
                    start: this.timelabels[timelabelIds[0]]['full_name'],
                    end: this.timelabels[_middleId]['full_name']
                },
                {
                    start: this.timelabels[_middleId]['full_name'],
                    end: this.timelabels[timelabelIds[
                        timelabelIds.length - 1]]['full_name']
                }
            ];
        } else if (timelabelIds.length > 0) {
            timelabelsForCagrs = [
                {
                    start: this.timelabels[timelabelIds[0]]['full_name'],
                    end: this.timelabels[timelabelIds[
                        timelabelIds.length - 1]]['full_name']
                }
            ];
        }

        for (let i = 0; i < variables.length; i++) {
            variable = variables[i];
            // TODO Check existing
            if (this.data[timescale] && this.data[timescale][variable]) {
                let data = this.data[timescale][variable]
                    .filter(function (el) {
                        let index = this.getTimelabelIndex(el['timestamp']);
                        return (index !== null
                                && timelabelIds.indexOf(index) != -1)
                                ? true : false;
                    }, this)
                    .map(function (el) {
                        let index = this.getTimelabelIndex(el['timestamp']);
                        return {
                            'name': this.timelabels[index]['full_name'],
                            'value': el['value'] // TODO Review for gr (VL)
                        }
                    }, this);
                let cagrs = timelabelsForCagrs.map(function (el) {
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

    public getData_Donut(period: Period,
                         variables: Array<string>): Array<Object> {
        if (!period['start'] || !period['end']) {
            return null;
        }
        let donuts = [];
        let variable: string = null;

        for (let i = 0; i < variables.length; i++) {
            variable = variables[i];
            let cagr = this.getCagrsForPeriod(variable,
                period['start'], period['end']);
            if (cagr) {
                donuts.push({
                    'name': this.variables[variable]['name'],
                    'value': cagr['value'] * 100 // !!!
                });
            }
        }
        return donuts;
    }

    public getData_VTable() {
        return {
            'variables': this.variables,
            'data': this.data,
            'timelabels': this.timelabels,
            // 'scales_order': this.scales, // ['annual', 'quarterly', 'monthly']
            // 'config': {
            //     'head': {
            //         'horizontal_order': Object.keys(this.variables), //['sales', 'volume', 'price'],
            //         'vertical_order': [
            //             {
            //                 'key': 'name',
            //                 'label': 'Name'
            //             },
            //             {
            //                 'key': 'metric',
            //                 'label': 'Metric'
            //             }
            //         ]
            //     }
            // }
        };
    }

    public getData_HTable() {
    }

    ////////////////////////////////

    /**
     *
     * @param variable: string
     * @param start: string
     * @param end: string
     * @returns {start: string, end: string, value: number}
     */
    public getCagrsForPeriod(variable: string, start: string, end: string): Cagr {
        start = start.toString();
        end = end.toString();
        for (let i = 0; i < this.cagrs[variable].length; i++) {
            if (this.cagrs[variable][i]['start'].toString() == start
                && this.cagrs[variable][i]['end'].toString() == end) {
                return this.cagrs[variable][i];
            }
        }
    }

    /**
     *
     * @param type: string
     * @returns {Array<string>}
     */
    public getVarsByType(type: string): Array<string> {
        // return ['Unit Size', 'Unit Volume', 'Value']; // TODO Remove
        let vars = [];
        for (let v in this.variables) {
            if (this.variables[v]['type'] == type) {
                vars.push(v);
            }
        }
        return vars;
    }

    public getTimelabelIndex(full_name: string) {
        return (full_name && this.timelabelsMap
        && this.timelabelsMap[full_name] !== undefined)
            ? this.timelabelsMap[full_name] : null;
    }

    public getInitialPeriod(scale: string): Period {
        // TODO Improve this method (VL)
        if (this.cagrPeriods && this.cagrPeriods.length > 0) {
            return this.cagrPeriods[this.cagrPeriods.length - 1];
        }
        return null;
    }

    ////////////////////////////////

    private digInitialData() {
        // TODO Implement method getInitialData() (VL)
    }

    private digMoreDecomposition() {
        // TODO Implement method digMoreDecomposition() (VL)
    }

    // TODO Move recreateScales() & _findKey() to common part or into Table model (VL)
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

    // public getDonutPeriodsLabel(): {start: string, end: string} {
    //     if (this.cagrPeriods.length > 0) {
    //         return {
    //             start: this.cagrPeriods[this.cagrPeriods.length - 1]['start'],
    //             end: this.cagrPeriods[this.cagrPeriods.length - 1]['end']
    //         };
    //     }
    //     return null;
    // }

    // public getTwoCagrPeriods(timelabelIds: Array<string|number>): Array<Object> {
    //     let timelabels = [];
    //
    //     if (timelabelIds.length >= 3) {
    //         let _middleId = timelabelIds[Math.floor((timelabelIds.length - 1) / 2)];
    //         timelabels = [
    //             {
    //                 start: this.timelabels[timelabelIds[0]]['name'],
    //                 end: this.timelabels[_middleId]['name']
    //             },
    //             {
    //                 start: this.timelabels[_middleId]['name'],
    //                 end: this.timelabels[timelabelIds[timelabelIds.length - 1]]['name']
    //             }
    //         ];
    //     } else if (timelabelIds.length > 0) {
    //         timelabels = [
    //             {
    //                 start: this.timelabels[timelabelIds[0]]['name'],
    //                 end: this.timelabels[timelabelIds[timelabelIds.length - 1]]['name']
    //             }
    //         ];
    //     }
    //     return timelabels;
    // }

    // public getShortTimeLablesForOutput(timescale: string): Array<number> {
    //     let longLables = this.getLongTimeLablesForOutput(timescale);
    //     if (longLables.length < 3) {
    //         return longLables;
    //     } else {
    //         return [
    //             longLables[0],
    //             longLables[Math.floor((longLables.length - 1) / 2)],
    //             longLables[longLables.length - 1],
    //         ];
    //     }
    // }

    // public getLongTimeLablesForOutput(timescale: string): Array<number> {
    //     let vars = this.getVarsByType('output');
    //     let timelables = [];
    //     if (vars && vars.length > 0) {
    //         timelables = this.data[timescale][vars[0]].map(function (el) {
    //             return this.getTimelabelIndex(el['timestamp']);
    //             //return el['timelabels_index'];
    //         }, this);
    //     }
    //     return timelables;
    // }
}
