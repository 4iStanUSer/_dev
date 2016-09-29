import {Component, OnInit, Input} from '@angular/core';
import {Chart} from './../../module/chart/';
import * as _ from 'lodash';

@Component({
    selector: 'bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit {

    private bar: Chart;

    private baseConfig: Object = {
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

        let config: Object = _.extend({}, this.baseConfig);
        config['title']['text'] = data['name'];
        config['series'][0]['name'] = data['name'];
        if (data['data'] && _.isArray(data['data'])) {
            for (let i=0; i<data['data'].length; i++) {
                config['series'][0]['data'].push([
                    data['data'][i]['name'],
                    data['data'][i]['value']
                ]);
            }
        }
        this.bar = new Chart(_.cloneDeep(config));
    };

    constructor() {
    }

    ngOnInit() {
    }

}
