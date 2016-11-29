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
