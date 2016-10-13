import {Component, OnInit, ViewChild} from '@angular/core';
import {DataManagerService} from './data-manager.service';
import {StaticDataService} from "../../common/service/static-data.service";
import {StateService, PageState} from "../../common/service/state.service";
import {WaterfallChartComponent} from "../../common/cmp/waterfall-chart/waterfall-chart.component";

@Component({
    selector: 'dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    private pageName: string = 'dashboard';
    private currMode: string = 'summary';
    private currTimeScale: string = 'annual';

    private localConfig: Object = {
        'modes': [
            {
                'key': 'summary',
                'name': 'Summary'
            },
            {
                'key': 'detailed',
                'name': 'Detailed'
            },
            {
                'key': 'drivers',
                'name': 'Drivers'
            }
        ],
    };

    @ViewChild('decomposition') decompositionObj: WaterfallChartComponent;

    private state: PageState;
    private lang: Object;
    private config: Object;

    private outputVars: Array<string> = [];
    private driverVars: Array<string> = [];

    private periods: Object = {
        'output_vars': {
            'short': [],
            'long': []
        }
    };

    public vTableData: Object = {};


    public period = {'start': 2016, 'end': 2020}; // TODO Review
    public summaryCagrsData: Array<Object> = null;
    // public summaryBarsData: Array<Object> = null;
    public summaryOutputsShortData: Array<Object> = null;

    public summaryDecompData: Object = null;

    /*---valueOrGrowthSwitch---*/
    public absOrRate: string = 'rate';
    public absOrRateSwitchData: Array<Object> = [
        {
            key: 'absolute',
            name: 'Absolute values',
            selected: false
        },
        {
            key: 'rate',
            name: 'Growth rates',
            selected: true
        }
    ];
    public absOrRateSwitchConfig: Object = {};

    public absOrRateSwitchChanged(e) {
        console.log('absOrRateSwitchChanged');

        this.absOrRate = e['key'];
        this.state.set('abs_or_rate', this.absOrRate);

        this.decompositionObj.changeMode(this.absOrRate);

        let outputVars = this.dm.getVarsByType('output');
        let timelabelsIds = this.dm.getShortTimeLablesForOutput(
            this.currTimeScale);

        if ('rate' == this.absOrRate && this.summaryCagrsData === null) {
            this.summaryCagrsData = this.dm.getData_Donut(timelabelsIds,
                outputVars);
        } else if (this.summaryOutputsShortData === null) {
            this.summaryOutputsShortData = this.dm.getData_Bar(timelabelsIds,
                outputVars);
        }
    }
    /*---.valueOrGrowthSwitch---*/
    /*---Decomposition---*/

    /*---.Decomposition---*/

    constructor(
        private dm: DataManagerService,
        private stateService: StateService, // TODO Review
        private sds: StaticDataService
    ) {
        this.state = this.stateService.getPageState(this.pageName);
        this.lang = this.sds.getLangPack(this.pageName);
        this.config = this.sds.getConfig(this.pageName);
    }

    ngOnInit() {

        let absOrRate = this.state.get('abs_or_rate');
        if (!absOrRate) {
            absOrRate = this.absOrRate;
            this.state.set('abs_or_rate', absOrRate);
        } else {
            this.absOrRate = absOrRate;
        }
        this.absOrRateSwitchData.forEach(function(el){
            if (this.absOrRate == el['key']) {
                el['selected'] = true;
            } else {
                el['selected'] = false;
            }
        }, this);

        let outputVars = this.dm.getVarsByType('output');
        let timelabelsIds = this.dm.getShortTimeLablesForOutput(
            this.currTimeScale);

        if ('rate' == this.absOrRate) {
            this.summaryCagrsData = this.dm.getData_Donut(timelabelsIds,
                outputVars);
        } else {
            this.summaryOutputsShortData = this.dm.getData_Bar(timelabelsIds,
                outputVars);
        }

        this.summaryDecompData = this.dm.getData_Waterfall(timelabelsIds,
            outputVars);

        //////////////////////////////////////////////////////////////////////


        // this.vTableData = this.dm.getData_VTable();


    }

    public changeMode(mode: string) {
        if (mode
            && this.localConfig['modes'].filter(function(el){
                return (el['key'] == mode) ? true : false;
            }, this) != -1)
        {
            this.currMode = mode;
        }
    }


    // NEW structures
    // private timelabels = [
    //     {
    //         name: 2010,
    //         timescale: 'annual',
    //         parent_index: null
    //     },
    //     {
    //         name: 2011,
    //         timescale: 'annual',
    //         parent_index: null
    //     },
    //     {
    //         name: 2012,
    //         timescale: 'annual',
    //         parent_index: null
    //     },
    //     {
    //         name: 2013,
    //         timescale: 'annual',
    //         parent_index: null
    //     },
    //
    //     //
    //
    //     {
    //         name: 'Q1',
    //         timescale: 'quarterly',
    //         parent_index: 0
    //     },
    //     {
    //         name: 'Q2',
    //         timescale: 'quarterly',
    //         parent_index: 0
    //     },
    //     {
    //         name: 'Q3',
    //         timescale: 'quarterly',
    //         parent_index: 0
    //     },
    //     {
    //         name: 'Q4',
    //         timescale: 'quarterly',
    //         parent_index: 0
    //     },
    //
    //     {
    //         name: 'Q1',
    //         timescale: 'quarterly',
    //         parent_index: 1
    //     },
    //     {
    //         name: 'Q2',
    //         timescale: 'quarterly',
    //         parent_index: 1
    //     },
    //     {
    //         name: 'Q3',
    //         timescale: 'quarterly',
    //         parent_index: 1
    //     },
    //     {
    //         name: 'Q4',
    //         timescale: 'quarterly',
    //         parent_index: 1
    //     },
    //
    //     {
    //         name: 'Q1',
    //         timescale: 'quarterly',
    //         parent_index: 2
    //     },
    //     {
    //         name: 'Q2',
    //         timescale: 'quarterly',
    //         parent_index: 2
    //     },
    //     {
    //         name: 'Q3',
    //         timescale: 'quarterly',
    //         parent_index: 2
    //     },
    //     {
    //         name: 'Q4',
    //         timescale: 'quarterly',
    //         parent_index: 2
    //     },
    //     {
    //         name: 'Q1',
    //         timescale: 'quarterly',
    //         parent_index: 3
    //     },
    //     {
    //         name: 'Q2',
    //         timescale: 'quarterly',
    //         parent_index: 3
    //     },
    //     {
    //         name: 'Q3',
    //         timescale: 'quarterly',
    //         parent_index: 3
    //     },
    //     {
    //         name: 'Q4',
    //         timescale: 'quarterly',
    //         parent_index: 3
    //     },
    //
    //     //
    //
    //     {
    //         name: 'Jan',
    //         timescale: 'monthly',
    //         parent_index: 4
    //     },
    //     {
    //         name: 'Feb',
    //         timescale: 'monthly',
    //         parent_index: 4
    //     },
    //     {
    //         name: 'Mar',
    //         timescale: 'monthly',
    //         parent_index: 4
    //     },
    //
    //     {
    //         name: 'Jan',
    //         timescale: 'monthly',
    //         parent_index: 8
    //     },
    //     {
    //         name: 'Feb',
    //         timescale: 'monthly',
    //         parent_index: 8
    //     },
    //     {
    //         name: 'Mar',
    //         timescale: 'monthly',
    //         parent_index: 8
    //     },
    // ];
    //
    // private data = {
    //     annual: {
    //         CPI: [
    //             {
    //                 'timelabels_index': 0,
    //                 'value': 13,
    //                 'gr': 15,
    //                 // 'color',
    //                 // 'isEditable',
    //                 // 'format'
    //             },
    //             {
    //                 'timelabels_index': 1,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 2,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 3,
    //                 'value': 13,
    //                 'gr': 15
    //             }
    //         ],
    //         GDP: [
    //             {
    //                 'timelabels_index': 0,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 1,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 2,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 3,
    //                 'value': 13,
    //                 'gr': 15
    //             }
    //         ]
    //     },
    //     quarterly: {
    //         CPI: [
    //             {
    //                 'timelabels_index': 4,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 5,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 6,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 7,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //         ],
    //         GDP: [
    //             {
    //                 'timelabels_index': 4,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 5,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 6,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 7,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //         ]
    //     },
    //     monthly: {
    //         CPI: [
    //             {
    //                 'timelabels_index': 20,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 21,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 22,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 23,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 24,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 25,
    //                 'value': 13,
    //                 'gr': 15
    //             }
    //         ],
    //         GDP: [
    //             {
    //                 'timelabels_index': 20,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 21,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 22,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 23,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 24,
    //                 'value': 13,
    //                 'gr': 15
    //             },
    //             {
    //                 'timelabels_index': 25,
    //                 'value': 13,
    //                 'gr': 15
    //             }
    //         ]
    //     }
    // };
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
    //     }
    // };
    //
    // private cagrs = {
    //     CPI: [
    //         {'start': 2013, 'end': 2016, 'value': 0.12},
    //         {'start': 2016, 'end': 2020, 'value': 0.13}
    //     ],
    //     GDP: [
    //         {'start': 2013, 'end': 2016, 'value': 0.10},
    //         {'start': 2016, 'end': 2020, 'value': 0.11}
    //     ]
    // };
    //
    // private decomposition = [
    //     {
    //         start: '2010',
    //         end: '2015',
    //         values: [
    //             {
    //                 name: 'Economic',
    //                 value: 2.15,
    //                 growth: 5,
    //                 children: null
    //             },
    //             {
    //                 name: 'Inflation',
    //                 value: 3.15,
    //                 growth: 4,
    //                 children: null
    //             },
    //             {
    //                 name: 'Pricing',
    //                 value: 4.15,
    //                 growth: 2,
    //                 children: null
    //             }
    //         ],
    //         volume: [
    //             {
    //                 name: 'Inflation',
    //                 value: 3.15,
    //                 growth: 2,
    //                 children: null
    //             },
    //             {
    //                 name: 'Pricing',
    //                 value: 4.15,
    //                 growth: 2,
    //                 children: null
    //             }
    //         ]
    //     }
    // ];



    // OLD structures
    // private donuts: Array<Object> = [
    //     {
    //         name: 'One',
    //         value: 86
    //     },
    //     {
    //         name: 'Two',
    //         value: 35
    //     },
    //     {
    //         name: 'Three',
    //         value: 49
    //     }
    // ];
    //
    // private bars: Array<Object> = [
    //     {
    //         name: 'Sales, $ MM',
    //         data: [
    //             {
    //                 name: '2013',
    //                 value: 14.2
    //             },
    //             {
    //                 name: '2015',
    //                 value: 16.1
    //             },
    //             {
    //                 name: '2020F',
    //                 value: 23.7
    //             }
    //         ]
    //     },
    //     {
    //         name: 'Volume, EQ Thousands',
    //         data: [
    //             {
    //                 name: '2013',
    //                 value: 12.2
    //             },
    //             {
    //                 name: '2015',
    //                 value: 18.1
    //             },
    //             {
    //                 name: '2020F',
    //                 value: 33.7
    //             }
    //         ]
    //     },
    //     {
    //         name: 'Price – per EQ, $',
    //         data: [
    //             {
    //                 name: '2013',
    //                 value: 0.05
    //             },
    //             {
    //                 name: '2015',
    //                 value: 0.06
    //             },
    //             {
    //                 name: '2020F',
    //                 value: 0.08
    //             }
    //         ]
    //     },
    // ];
    //
    // private waterfall: Object = {
    //     name: 'Decomposition 2015-2020',
    //     pipsName: '%',
    //     data: [
    //         {
    //             name: '2015',
    //             value: 100
    //         }, {
    //             name: 'Economy',
    //             value: 10
    //         }, {
    //             name: 'Demographic',
    //             value: 12
    //         }, {
    //             name: 'Inflation',
    //             value: 15
    //         }, {
    //             name: 'Distribution',
    //             value: 4
    //         }, {
    //             name: 'Pricing',
    //             value: -5
    //         }, {
    //             name: '2020'
    //         }
    //     ]
    // };
    //
    // private accordion_table: Object = {
    //     'head': {
    //         'rows': [
    //             {
    //                 'meta': {
    //                     name: 'Driver'
    //                 },
    //                 'cells': [
    //                     {
    //                         'value': 'Real GDP per capita',
    //                         'type': 'string',
    //                         'options': {}
    //                     },
    //                     {
    //                         'value': 'CPI',
    //                         'type': 'string',
    //                         'options': {}
    //                     }
    //                 ],
    //                 'options': {}
    //             },
    //             {
    //                 'meta': {
    //                     name: 'Metric'
    //                 },
    //                 'cells': [
    //                     {
    //                         'value': 'Const LC',
    //                         'type': 'string',
    //                         'options': {}
    //                     },
    //                     {
    //                         'value': 'Index',
    //                         'type': 'string',
    //                         'options': {}
    //                     }
    //                 ],
    //                 'options': {}
    //             }
    //         ],
    //         'options': {}
    //     },
    //     'body': {
    //         'rows': [
    //             {
    //                 'meta': {
    //                     name: '2013'
    //                 },
    //                 'cells': [
    //                     {
    //                         'value': 55458,
    //                         'type': 'int',
    //                         'options': {}
    //                     },
    //                     {
    //                         'value': 103.9,
    //                         'type': 'float',
    //                         'options': {}
    //                     }
    //                 ],
    //                 'children': [
    //                     {
    //                         'meta': {
    //                             name: 'Q1'
    //                         },
    //                         'cells': [
    //                             {
    //                                 'value': 12458,
    //                                 'type': 'int',
    //                                 'options': {}
    //                             },
    //                             {
    //                                 'value': 103.9,
    //                                 'type': 'float',
    //                                 'options': {}
    //                             }
    //                         ],
    //                         'children': [
    //                             {
    //                                 'meta': {
    //                                     name: 'January'
    //                                 },
    //                                 'cells': [
    //                                     {
    //                                         'value': 12458,
    //                                         'type': 'int',
    //                                         'options': {}
    //                                     },
    //                                     {
    //                                         'value': 103.9,
    //                                         'type': 'float',
    //                                         'options': {}
    //                                     }
    //                                 ],
    //                                 'children': [],
    //                                 'options': {}
    //                             },
    //                             {
    //                                 'meta': {
    //                                     name: 'February'
    //                                 },
    //                                 'cells': [
    //                                     {
    //                                         'value': 12458,
    //                                         'type': 'int',
    //                                         'options': {}
    //                                     },
    //                                     {
    //                                         'value': 103.9,
    //                                         'type': 'float',
    //                                         'options': {}
    //                                     }
    //                                 ],
    //                                 'children': [],
    //                                 'options': {}
    //                             }
    //                         ],
    //                         'options': {}
    //                     },
    //                     {
    //                         'meta': {
    //                             name: 'Q2'
    //                         },
    //                         'cells': [
    //                             {
    //                                 'value': 10256,
    //                                 'type': 'int',
    //                                 'options': {}
    //                             },
    //                             {
    //                                 'value': 103.9,
    //                                 'type': 'float',
    //                                 'options': {}
    //                             }
    //                         ],
    //                         'children': [],
    //                         'options': {}
    //                     }
    //                 ],
    //                 'options': {}
    //             },
    //             {
    //                 'meta': {
    //                     name: '2014'
    //                 },
    //                 'cells': [
    //                     {
    //                         'value': 55102,
    //                         'type': 'int',
    //                         'options': {}
    //                     },
    //                     {
    //                         'value': 109.4,
    //                         'type': 'float',
    //                         'options': {}
    //                     }
    //                 ],
    //                 'options': {}
    //             }
    //         ],
    //         'options': {}
    //     },
    //     'options': {}
    // };

}

