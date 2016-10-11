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

    private activeMode: Object = null;
    private modes: Array<Object> = [];
    private baseName: string = null;
    private start: string = null;
    private end: string = null;
    private d: {[s: string]: Array<Object>} = {};

    // pipsName: string = null;

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

        let config: Object = _.cloneDeep(this.baseConfig);
        this.modes = data['modes'];
        this.activeMode = this.modes[0]; //
        this.baseName = data['base_name'];
        this.start = data['start'];
        this.end = data['end'];
        this.d = {};
        this.modes.forEach(function(item){
            this.d[item['key']] = data[item['key']];
        }, this);

        let name = this.baseName + ' ' + this.start.toString() +
            '-' + this.end.toString();

        config['title']['text'] = name;
        config['series'][0] = this._getSeriesForMode(this.activeMode);
        this.waterfall = new Chart(_.cloneDeep(config));
    };

    private onModeChange(e) {
        this.activeMode = e;
        let newSeries = this._getSeriesForMode(this.activeMode);

        this.waterfall.removeSerie(0);
        this.waterfall.addSerie(_.cloneDeep(newSeries));
    }

    private _getSeriesForMode(mode: Object){
        let modeKey = mode['key'];
        let newSeries = _.cloneDeep(this.baseConfig['series'][0]);
        newSeries['dataLabels']['formatter'] = this._formatter(mode['metric']);
        if (modeKey in this.d) {
            for (let i=0; i<this.d[modeKey].length; i++) {
                if (i == this.d[modeKey].length - 1) {
                    newSeries['data'].push({
                        name: this.d[modeKey][i]['name'],
                        isSum: true
                    });
                } else {
                    newSeries['data'].push({
                        name: this.d[modeKey][i]['name'],
                        y: this.d[modeKey][i]['value']
                    });
                }
            }
        }
        return newSeries;
    }

    private _formatter(points) {
        return function(){
            return this.y + ' ' + points.toString();
        };
    }

    constructor() { }

    ngOnInit() {
    }

}
