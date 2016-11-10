import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Chart} from './../../module/chart/';


interface BarChartDataInput {
    name: string;
    value: number;
}

@Component({
    selector: 'bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit {

    private chart: Chart = null;

    private chartConfig: Object = {
        chart: {
            type: 'column'
        },
        title: {
            text: null
        },
        xAxis: {
            type: 'category',
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
                name: null,
                data: [],
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        ]
    };

    @Input() set data(data: Array<BarChartDataInput>) {
        console.info('BarChartComponent: set data');

        let dataToPush = [];
        for (let i = 0; i < data.length; i++) {
            dataToPush.push([
                data[i]['name'].toString(),
                data[i]['value']
            ]);
        }
        this.chartConfig['series'][0]['data'] = dataToPush;
        this.chart = new Chart(this.chartConfig)
    };

    constructor() { }

    ngOnInit() {

    }
}



// interface BarChartDataInput { // TODO Remake (VL)
//     name: string;
//     variable: {name: string, metric: string};
//     cagrs: Array<{start: string, end: string, value: number}>;
//     data: Array<{name: string, value: number}>;
// }
//
// interface BarChartConfig {
//     showGrowth?: boolean;
//     showCagrs?: boolean;
// }
//
// @Component({
//     selector: 'bar-chart',
//     templateUrl: './bar-chart.component.html',
//     styleUrls: ['./bar-chart.component.css']
// })
// export class BarChartComponent implements OnInit { // TODO Implement 2 modes: short & full (cagrs for middle point too)
//
//     private _c: BarChartConfig = {
//         showGrowth: false,
//         showCagrs: true
//     };
//
//     private blocks: Array<{
//         name: string;
//         variable: Object;
//         cagrs: Array<Object>,
//         chart: Chart
//     }> = [];
//
//     private baseChartConfig: Object = {
//         chart: {
//             type: 'column'
//         },
//         title: {
//             text: ''
//         },
//         xAxis: {
//             type: 'category',
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
//             name: '',
//             data: [],
//             dataLabels: {
//                 enabled: true,
//                 format: '{point.y}'
//             }
//         }]
//     };
//
//     // @Output('click-expand') clickExpand = new EventEmitter();
//
//     // @Input() set config(c: BarChartConfig) { // TODO Realize this
//     //     _.extend(this._c, c);
//     // }
//
//     @Input() set data(data: Array<BarChartDataInput>) {
//         console.info('BarChartComponent: set data');
//         this.blocks = [];
//         for (let i = 0; i < data.length; i++) {
//             let config: Object = _.cloneDeep(this.baseChartConfig);
//             // config['title']['text'] = data[i]['name'];
//             // config['series'][0]['name'] = data[i]['name'];
//             if (data[i]['data'] && _.isArray(data[i]['data'])) {
//                 for (let j = 0; j < data[i]['data'].length; j++) {
//                     config['series'][0]['data'].push([
//                         data[i]['data'][j]['name'].toString(),
//                         data[i]['data'][j]['value']
//                     ]);
//                 }
//             }
//             this.blocks.push({
//                 name: data[i]['name'],
//                 variable: data[i]['variable'],
//                 cagrs: data[i]['cagrs'],
//                 chart: new Chart(_.cloneDeep(config))
//             });
//         }
//     };
//
//     // private onExpandButtonClick(blockId: number) {
//     //     console.info('BarChartComponent "click-expand" event');
//     //     this.clickExpand.emit({
//     //         'name': (blockId !== null && this.blocks[blockId])
//     //             ? this.blocks[blockId]['name'] : null
//     //     });
//     // }
//
//     constructor() {
//     }
//
//     ngOnInit() {
//     }
//
// }
