import {Component, OnInit, Input} from '@angular/core';
import {Chart} from './../../module/chart/';
import * as _ from 'lodash';

@Component({
    selector: 'donut-chart',
    templateUrl: './donut-chart.component.html',
    styleUrls: ['./donut-chart.component.css']
})
export class DonutChartComponent implements OnInit {
    private donuts: Array<Chart> = [];
    private baseConfig: Object = {
        chart: {
            type: 'pie',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        tooltip: {
            enabled: false,
        },
        plotOptions: {
            pie: {
                innerSize: '70%',
                dataLabels: {
                    distance: -150,
                    enabled: true,
                    format: '{point.percentage:.1f} %',
                }
            }
        },
        title: {
            text: ''
        },
        series: []
    };

    @Input() set data(series: Array<any>) {
        console.info('DonutChartComponent: set data');
        this.donuts = []; // TODO REMAKE - without recreating
        let config: Object = {};
        for (let i = 0; i<series.length; i++) {
            config = _.extend({}, this.baseConfig);
            // s = series[i];
            config['title']['text'] = series[i]['name'];
            config['series'] = [
                {
                    name: series[i]['name'],
                    data: [{
                        name: series[i]['name'],
                        y: parseInt(series[i]['value']) // less than 100
                    }, {
                        name: 'Other',
                        y: 100 - parseInt(series[i]['value']),
                        dataLabels: {
                            enabled: false
                        }
                    }]
                }
            ];
            this.donuts.push(new Chart(_.cloneDeep(config)));
        }
    };

    constructor() { }

    ngOnInit() { }

}
