import {Component, OnInit, Input} from '@angular/core';
import {Chart,Highcharts} from './../../module/chart/';
import * as _ from 'lodash';

// http://www.highcharts.com/docs/chart-and-series-types/waterfall-series

@Component({
    selector: 'waterfall-chart',
    templateUrl: './waterfall-chart.component.html',
    styleUrls: ['./waterfall-chart.component.css']
})
export class WaterfallChartComponent implements OnInit {

    private waterfall: Chart;

    private baseConfig: Object = {
        chart: {
            type: 'waterfall'
        },

        title: {
            text: 'Highcharts Waterfall'
        },

        xAxis: {
            type: 'category'
        },

        yAxis: {
            title: {
                text: 'USD'
            }
        },

        legend: {
            enabled: false
        },

        tooltip: {
            pointFormat: '<b>${point.y:,.2f}</b> USD'
        },

        series: [{
            upColor: Highcharts.getOptions().colors[2],
            color: Highcharts.getOptions().colors[3],
            data: [{
                name: 'Start',
                y: 120000
            }, {
                name: 'Product Revenue',
                y: 569000
            }, {
                name: 'Service Revenue',
                y: 231000
            }, {
                name: 'Positive Balance',
                y: 231000
                // isIntermediateSum: true,
                // color: Highcharts.getOptions().colors[1]
            }, {
                name: 'Fixed Costs',
                y: -342000
            }, {
                name: 'Variable Costs',
                y: -233000
            }, {
                name: 'Balance',
                isSum: true,
                color: '#0066FF'
                // isSum: true,
                // color: Highcharts.getOptions().colors[2]
                // y: -233000,
                // isIntermediateSum: true
            }],
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return Highcharts.numberFormat(this.y / 1000, 0, ',') + 'k';
                },
                style: {
                    fontWeight: 'bold'
                }
            },
            pointPadding: 0
        }]
    };

    @Input() set data(data: Array<any>) {
        console.info('WaterfallChartComponent: set data');

        let config: Object = _.extend({}, this.baseConfig);
        // config['title']['text'] = data['name'];
        // config['series'][0]['name'] = data['name'];
        // if (data['data'] && _.isArray(data['data'])) {
        //     for (let i=0; i<data['data'].length; i++) {
        //         config['series'][0]['data'].push([
        //             data['data'][i]['name'],
        //             data['data'][i]['value']
        //         ]);
        //     }
        // }
        this.waterfall = new Chart(_.cloneDeep(config));
    };

    constructor() { }

    ngOnInit() {
    }

}
