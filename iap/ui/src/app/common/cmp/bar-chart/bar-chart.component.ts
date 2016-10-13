import {Component, OnInit, Input} from '@angular/core';
import {Chart} from './../../module/chart/';
import * as _ from 'lodash';

@Component({
    selector: 'bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit {

    private blocks: Array<{
        name: string;
        cagrs: Array<Object>,
        chart: Chart
    }> = [];

    private baseChartConfig: Object = {
        chart: {
            type: 'column'
        },
        title: {
            text: ''
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
        series: [{
            name: '',
            data: [],
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }]
    };

    @Input() set data(data: Array<any>) {
        console.info('BarChartComponent: set data');
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let config: Object = _.cloneDeep(this.baseChartConfig);
            // config['title']['text'] = data[i]['name'];
            // config['series'][0]['name'] = data[i]['name'];
            if (data[i]['data'] && _.isArray(data[i]['data'])) {
                for (let j = 0; j < data[i]['data'].length; j++) {
                    config['series'][0]['data'].push([
                        data[i]['data'][j]['name'],
                        data[i]['data'][j]['value']
                    ]);
                }
            }
            this.blocks.push({
                name: data[i]['name'],
                cagrs: data[i]['cagrs'],
                chart: new Chart(_.cloneDeep(config))
            });
        }
    };

    constructor() {
    }

    ngOnInit() {
    }

}
