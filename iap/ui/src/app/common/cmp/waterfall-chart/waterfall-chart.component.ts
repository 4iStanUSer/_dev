import {Component, OnInit, Input} from '@angular/core';
import {Chart,Highcharts} from './../../module/chart/';
import * as _ from 'lodash';

// http://www.highcharts.com/docs/chart-and-series-types/waterfall-series


// TODO Implement State feature for Waterfall Chart
interface WaterfallChartState {
    currentMode: string;
    currentVariable: string;
}


@Component({
    selector: 'waterfall-chart',
    templateUrl: './waterfall-chart.component.html',
    styleUrls: ['./waterfall-chart.component.css']
})
export class WaterfallChartComponent implements OnInit {

    private localConfig: Object = {
        'modes': [
            {
                'key': 'growth',
                'name': 'Growth rate'
            },
            {
                'key': 'value',
                'name': 'Absolute'
            }
        ],
    };

    private baseChartConfig: Object = {
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

    private waterfall: Chart;

    private currentVar: string = null;
    private currentMode: Object = null;
    private variables: Array<string> = [];
    private modes: Array<Object> = [];

    private baseName: string = null;
    private start: string = null;
    private end: string = null;
    private d: {[s: string]: Array<Object>} = {};

    @Input() set data(data: Object) {
        console.info('WaterfallChartComponent: set data');

        let config: Object = _.cloneDeep(this.baseChartConfig);

        // this.modes = data['modes'];
        this.modes = this.localConfig['modes'];
        this.variables = data['variables'];
        this.baseName = data['base_name'];
        this.start = data['start'];
        this.end = data['end'];
        this.d = {};

        this.currentMode = this.modes[0]; // TODO Rewrite
        this.currentVar = this.variables[0]; // TODO Rewrite

        this.variables.forEach(function(variable){
            this.d[variable['key']] = data[variable['key']];
        }, this);

        let name = this.baseName + ' ' + this.start.toString() +
            '-' + this.end.toString();

        config['title']['text'] = name;
        config['series'][0] = this._getSeriesForMode(this.currentVar,
            this.currentMode);
        this.waterfall = new Chart(_.cloneDeep(config));
    };

    public changeMode(mode: string) {
        console.log(mode);
        let m = ('absolute' == mode) ? 'value' : 'growth';

        if (m != this.currentMode['key']) {
            this.modes.forEach(function(el, i){
                if (m == el['key']) {
                    this.currentMode = this.modes[i];
                }
            }, this);
            let newSeries = this._getSeriesForMode(this.currentVar,
                this.currentMode);
            this.waterfall.removeSerie(0);
            this.waterfall.addSerie(_.cloneDeep(newSeries));
        }
    }

    private onVariableChange(variable) {
        if (variable != this.currentVar) {
            this.currentVar = variable;
            let newSeries = this._getSeriesForMode(this.currentVar,
                this.currentMode);

            this.waterfall.removeSerie(0);
            this.waterfall.addSerie(_.cloneDeep(newSeries));
        }
    }

    private _getSeriesForMode(variable: Object, mode: Object) {
        // let modeKey = mode['key'];
        let newSeries = _.cloneDeep(this.baseChartConfig['series'][0]);
        let metric = (mode['key']== 'growth') ? '%' : variable['metric'];

        newSeries['dataLabels']['formatter'] = this._formatter(metric);
        if (variable['key'] in this.d) {
            for (let i=0; i<this.d[variable['key']].length; i++) {
                if (i == this.d[variable['key']].length - 1) {
                    newSeries['data'].push({
                        name: this.d[variable['key']][i]['name'],
                        isSum: true
                    });
                } else {
                    newSeries['data'].push({
                        name: this.d[variable['key']][i]['name'],
                        y: this.d[variable['key']][i]['value']
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
