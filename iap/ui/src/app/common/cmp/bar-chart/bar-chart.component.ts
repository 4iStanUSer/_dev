import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Chart} from './../../module/chart/';
import * as _ from 'lodash';

interface BarChartConfig {
    showGrowth?: boolean;
    showCagrs?: boolean;
}

@Component({
    selector: 'bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit {

    private _c: BarChartConfig = {
        showGrowth: false,
        showCagrs: true
    };

    private blocks: Array<{
        name: string;
        variable: Object;
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

    @Output('click-expand') clickExpand = new EventEmitter();

    // @Input() set config(c: BarChartConfig) { // TODO Realize this
    //     _.extend(this._c, c);
    // }

    @Input() set data(data: Array<any>) {
        console.info('BarChartComponent: set data');

        for (let i = 0; i < data.length; i++) {
            let config: Object = _.cloneDeep(this.baseChartConfig);
            // config['title']['text'] = data[i]['name'];
            // config['series'][0]['name'] = data[i]['name'];
            if (data[i]['data'] && _.isArray(data[i]['data'])) {
                for (let j = 0; j < data[i]['data'].length; j++) {
                    config['series'][0]['data'].push([
                        data[i]['data'][j]['name'].toString(),
                        data[i]['data'][j]['value']
                    ]);
                }
            }
            this.blocks.push({
                name: data[i]['name'],
                variable: data[i]['variable'],
                cagrs: data[i]['cagrs'],
                chart: new Chart(_.cloneDeep(config))
            });
        }
    };

    private onExpandButtonClick(blockId: number) {
        console.info('BarChartComponent "click-expand" event');
        this.clickExpand.emit({
            'name': (blockId !== null && this.blocks[blockId])
                ? this.blocks[blockId]['name'] : null
        });
    }

    constructor() {
    }

    ngOnInit() {
    }

}
