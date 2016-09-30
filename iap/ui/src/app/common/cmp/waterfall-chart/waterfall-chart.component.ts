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

    pipsName: string = null;

    private baseConfig: Object = {
        chart: {
            type: 'waterfall'
        },
        title: {
            text: ''
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
        series: [{
            upColor: Highcharts.getOptions().colors[2],
            color: Highcharts.getOptions().colors[3],
            data: [],
            dataLabels: {
                enabled: true,
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
        config['title']['text'] = data['name'];

        this.pipsName = data['pipsName'];

        config['series'][0]['dataLabels']['formatter'] = this._formatter(this.pipsName);

        if (data['data'] && _.isArray(data['data'])) {
            for (let i=0; i<data['data'].length; i++) {
                if (i == data['data'].length - 1) {
                    config['series'][0]['data'].push({
                        name: data['data'][i]['name'],
                        isSum: true
                    });
                } else {
                    config['series'][0]['data'].push({
                        name: data['data'][i]['name'],
                        y: data['data'][i]['value']
                    });
                }
            }
        }
        this.waterfall = new Chart(_.cloneDeep(config));
    };

    private _formatter(pips) {
        return function(){
            return this.y + pips;
        };
    }

    constructor() { }

    ngOnInit() {
    }

}
