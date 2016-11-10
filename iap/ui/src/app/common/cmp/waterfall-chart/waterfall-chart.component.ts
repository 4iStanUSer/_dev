import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Chart} from './../../module/chart/';

// http://www.highcharts.com/docs/chart-and-series-types/waterfall-series

export type WaterfallChartDataInput = Array<{
    name: string;
    value: number;
    metric?: string;
}>;

@Component({
    selector: 'waterfall-chart',
    templateUrl: './waterfall-chart.component.html',
    styleUrls: ['./waterfall-chart.component.css']
})
export class WaterfallChartComponent implements OnInit {

    private chart: Chart = null;

    private metric: string = null;

    private chartConfig: Object = {
        chart: {
            type: 'waterfall'
        },
        title: {
            text: null
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            visible: false
        },
        legend: {
            enabled: false
        },
        tooltip: {
            enabled: false
        },
        series: [
            {
                data: [],
                dataLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold'
                    }
                },
                pointPadding: 0,
                // upColor: Highcharts.getOptions().colors[2],
                // color: Highcharts.getOptions().colors[3],
            }
        ]
    };

    @Input() set data(data: WaterfallChartDataInput) {
        console.info('WaterfallChartComponent: set data');

        let dataToPush = [];
        let l = data.length;
        if (l>0) {
            this.metric = (data[0]['metric']) ? data[0]['metric'] : null;
            for (let i = 0; i < l; i++) {
                if (i == l - 1) {
                    dataToPush.push({
                        name: data[i]['name'],
                        isSum: true
                    });
                } else {
                    dataToPush.push({
                        name: data[i]['name'],
                        y: data[i]['value']
                    });
                }
            }
        }

        this.chartConfig['series'][0]['data'] = dataToPush;
        this.chartConfig['series'][0]['dataLabels']['formatter'] =
            this._formatter(this.metric);
        this.chart = new Chart(this.chartConfig);
    }

    private _formatter(points) {
        if (points && points.length) {
            return function () {
                return this.y + ' ' + points.toString();
            };
        } else {
            return function () {
                return this.y;
            };
        }
    }

    constructor() {
    }

    ngOnInit() {
    }
}





// @Component({
//     selector: 'waterfall-chart',
//     templateUrl: './waterfall-chart.component.html',
//     styleUrls: ['./waterfall-chart.component.css']
// })
// export class WaterfallChartComponent implements OnInit {


// // TODO Implement State feature for Waterfall Chart
// interface WaterfallChartState {
//     currentMode: string;
//     currentVariable: string;
// }
//
// interface WaterfallChartData {
//
// }
//
//
// @Component({
//     selector: 'waterfall-chart',
//     templateUrl: './waterfall-chart.component.html',
//     styleUrls: ['./waterfall-chart.component.css']
// })
// export class WaterfallChartComponent implements OnInit {
//
//     private localConfig: Object = {
//         'modes': [
//             {
//                 'key': 'rate',
//                 'name': 'Growth rate'
//             },
//             {
//                 'key': 'abs',
//                 'name': 'Absolute'
//             }
//         ],
//     };
//
//     private baseChartConfig: Object = {
//         chart: {
//             type: 'waterfall'
//         },
//         title: {
//             text: ''
//         },
//         xAxis: {
//             type: 'category'
//         },
//         yAxis: {
//             visible: false
//         },
//         legend: {
//             enabled: false
//         },
//         tooltip: {
//             enabled: false
//         },
//         series: [{
//             upColor: Highcharts.getOptions().colors[2],
//             color: Highcharts.getOptions().colors[3],
//             data: [],
//             dataLabels: {
//                 enabled: true,
//                 style: {
//                     fontWeight: 'bold'
//                 }
//             },
//             pointPadding: 0
//         }]
//     };
//
//     private waterfall: Chart;
//     private driversChanges: Array<Object> = [];
//
//     private currentVar: string = null;
//     private currentMode: Object = null;
//     private variables: Array<string> = [];
//     private modes: Array<Object> = [];
//
//     private baseName: string = null;
//     private start: string = null;
//     private end: string = null;
//     private d: {[s: string]: Array<Object>} = {};
//
//     @Output('click-expand') clickExpand = new EventEmitter();
//
//     @Input() set data(data: Object) {
//         console.info('WaterfallChartComponent: set data');
//
//         let config: Object = _.cloneDeep(this.baseChartConfig);
//
//         // this.modes = data['modes'];
//         this.modes = this.localConfig['modes'];
//         this.baseName = data['base_name'];
//         this.start = data['start'];
//         this.end = data['end'];
//         this.variables = [];
//         this.d = {};
//
//         data['vars'].forEach(function(v){
//             this.d[v['key']] = v['values'];
//             this.variables.push({
//                 'name': v['name'],
//                 'key': v['key'],
//                 'metric': v['metric'],
//                 'multiplier': v['multiplier'],
//             });
//         }, this);
//
//         this.currentMode = this.modes[0]; // TODO Rewrite
//         this.currentVar = this.variables[0]; // TODO Rewrite
//
//         let name = this.baseName + ' ' + this.start.toString() +
//             '-' + this.end.toString();
//
//         config['title']['text'] = name;
//         config['series'][0] = this._getSeriesForMode(this.currentVar,
//             this.currentMode);
//         this.waterfall = new Chart(_.cloneDeep(config));
//
//         this.driversChanges = this._getDriversChangesForMode(this.currentVar,
//             this.currentMode);
//     };
//
//     public changeMode(mode: string) {
//         let m = ('absolute' == mode) ? 'abs' : 'rate';
//
//         if (m != this.currentMode['key']) {
//             this.modes.forEach(function(el, i){
//                 if (m == el['key']) {
//                     this.currentMode = this.modes[i];
//                 }
//             }, this);
//             let newSeries = this._getSeriesForMode(this.currentVar,
//                 this.currentMode);
//
//             this.waterfall.removeSerie(0);
//             this.waterfall.addSerie(_.cloneDeep(newSeries));
//
//             this.driversChanges = this._getDriversChangesForMode(
//                 this.currentVar,this.currentMode);
//         }
//     }
//
//     private onVariableChange(variable) {
//         if (variable != this.currentVar) {
//             this.currentVar = variable;
//             let newSeries = this._getSeriesForMode(this.currentVar,
//                 this.currentMode);
//
//             this.waterfall.removeSerie(0);
//             this.waterfall.addSerie(_.cloneDeep(newSeries));
//
//             this.driversChanges = this._getDriversChangesForMode(
//                 this.currentVar,this.currentMode);
//         }
//     }
//     private onExpandButtonClick(e) {
//         console.info('WaterfallChartComponent "click-expand" event');
//         this.clickExpand.emit({
//             'start': this.start,
//             'end': this.end
//         });
//     }
//
//     private _getSeriesForMode(variable: Object, mode: Object) {
//         let newSeries = _.cloneDeep(this.baseChartConfig['series'][0]);
//         let metric = (mode['key']== 'rate') ? '%' : variable['metric'];
//         let vKey = (mode['key']== 'rate') ? 'impact_rate' : 'impact_abs';
//
//         newSeries['dataLabels']['formatter'] = this._formatter(metric);
//         if (variable['key'] in this.d) {
//             for (let i=0; i<this.d[variable['key']].length; i++) {
//                 if (i == this.d[variable['key']].length - 1) {
//                     newSeries['data'].push({
//                         name: this.d[variable['key']][i]['name'],
//                         isSum: true
//                     });
//                 } else {
//                     newSeries['data'].push({
//                         name: this.d[variable['key']][i]['name'],
//                         y: this.d[variable['key']][i][vKey]
//                     });
//                 }
//             }
//         }
//         return newSeries;
//     }
//     private _getDriversChangesForMode(variable: Object,
//                                       mode: Object): Array<Object> { // TODO Interface
//         let vKey = (mode['key']== 'rate') ? 'change_rate' : 'change_abs';
//         let changes = [];
//
//         if (variable['key'] in this.d) {
//             for (let i=1; i<this.d[variable['key']].length -1; i++) {
//                 changes.push({
//                     name: this.d[variable['key']][i]['name'],
//                     value: this.d[variable['key']][i][vKey],
//                     metric: (mode['key']== 'rate') ? '%' : variable['metric']
//                 });
//             }
//         }
//         return changes;
//     }
//
//     private _formatter(points) {
//         return function(){
//             return this.y + ' ' + points.toString();
//         };
//     }
//
//     constructor() { }
//
//     ngOnInit() {
//     }
//
// }
