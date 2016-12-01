import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Chart} from './../../module/chart/';


export type BarChartDataInput = Array<{
    name: string;
    value: number;
}>;

@Component({
    selector: 'bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
/**
 * Simple wrapper component for Bars Chart.
 * http://www.highcharts.com/demo/column-basic
 * Main aim - configure chart options, process/transform input data
 * for using inside Highcharts library.
 * Should be used inside template of page/tab components
 */
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

    @Input() set data(data: BarChartDataInput) {
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
