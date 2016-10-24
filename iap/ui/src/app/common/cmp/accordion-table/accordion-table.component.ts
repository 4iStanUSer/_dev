import {Component, OnInit, Input} from '@angular/core';
import * as _ from 'lodash';
import {ITable, TblRow} from './interfaces';
import {RowModel} from './row.model';

@Component({
    selector: 'accordion-table',
    templateUrl: './accordion-table.component.html',
    styleUrls: ['./accordion-table.component.css']
})
export class AccordionTableComponent implements OnInit {

    private config: Object = {};

    private depthLevels: Array<number> = [];

    private visibleLevels: Array<number> = [0, 1];

    private columns: Array<string> = [];

    private headRows: Array<RowModel> = [];

    private bodyRows: {[index: number]: RowModel} = {};

    private bodyRowsOrder: Array<number> = [];

    constructor() {
    }

    ngOnInit() {
    }

    @Input() set data(d: Object) {
        this.config = d['config'];
        this.headRows = [];
        this.bodyRowsOrder = [];
        this.bodyRows = {};

        this.columns = this.config['head']['horizontal_order'];

        // Fill head rows
        let headRow: TblRow = null;
        let verticalItem: Object = null;
        let varName: string = null;
        for (let j = 0; j < this.config['head']['vertical_order'].length; j++) {
            verticalItem = this.config['head']['vertical_order'][j];
            headRow = {
                'meta': {
                    'label': verticalItem['label']
                },
                'data': {},
                'options': {}
            };
            for (let i = 0; i < this.columns.length; i++) {
                varName = this.columns[i];
                headRow['data'][varName] = {
                    value: d['variables'][varName][verticalItem['key']],
                    type: 'string',
                    options: {}
                };
            }
            this.headRows.push(
                new RowModel(null, headRow, null, true)
            );
        }

        // Add values into 'timelabels'
        let valueObj: Object = null;
        for (let scale in  d['data']) {
            for (let variable in d['data'][scale]) {
                for (let i = 0; i < d['data'][scale][variable].length; i++) {
                    valueObj = d['data'][scale][variable][i];

                    let index = this.getTimeLabelIndex(d['timelabels'],
                        valueObj['timestamp']);
                    if (index !== null) {
                        if (!('values' in d['timelabels'][index])) {
                            d['timelabels'][index]['values'] = {};
                        }
                        d['timelabels'][index]['values'][variable] = valueObj;
                    }

                    // if (!('values' in d['timelabels'][valueObj['timelabels_index']])) {
                    //     d['timelabels'][valueObj['timelabels_index']]['values'] = {};
                    // }
                    // d['timelabels'][valueObj['timelabels_index']]['values'][variable] = valueObj;

                }
            }
        }
        for (let i = 0; i < d['timelabels'].length; i++) {
            this.addBodyRow(d['timelabels'], i);
        }
    }

    private getTimeLabelIndex(timelabels: Array<Object>, name: string) {
        for (let i = 0; i < timelabels.length; i++) {
            if (timelabels[i]['name'] == name) { // TODO Remake 'name'->'full_name' (VL)
                return i;
            }
        }
        return null;
    }

    private visibleDataRows(){
        return this.bodyRowsOrder.filter(function(el){
            return (this.bodyRows[el].isShown); // this.visibleLevels.indexOf(this.bodyRows[el].depth) !== -1 TODO Levels
        }, this);
    }

    private addBodyRow(temp: Array<Object>,
                       index: number,
                       parent: RowModel = null) {
        if (!(temp[index]) || this.bodyRows[index]) {
            return;
        }

        let row = {
            'meta': {
                'label': temp[index]['name']
            },
            'data': {},
            'options': {}
        };
        for (let variable in temp[index]['values']) {
            row['data'][variable] = {
                'value': temp[index]['values'][variable]['value'], // !!!
                'type': 'string',
                'options': {}
            };
        }
        this.bodyRowsOrder.push(index);
        this.bodyRows[index] = new RowModel(index, row, parent);

        if (this.depthLevels.indexOf(this.bodyRows[index].depth) == -1) {
            this.depthLevels.push(this.bodyRows[index].depth);
        }
        if (temp[index]['children']) {
            for (let i = 0; i < temp[index]['children'].length; i++) {
                this.addBodyRow(
                    temp,
                    temp[index]['children'][i],
                    this.bodyRows[index]
                );
            }
        }
    }

    public range(start: number, stop?: number, step?: number) {
        if (typeof stop == 'undefined') {
            stop = start;
            start = 0;
        }
        if (typeof step == 'undefined') {
            step = 1;
        }
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }
        var result = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.push(i);
        }
        return result;
    };

}
