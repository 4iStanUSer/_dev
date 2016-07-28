import { Component, Input, Output, ElementRef,
    EventEmitter } from '@angular/core';
import * as _ from 'lodash';

/*
 * TS - TimeSeries
 * <timeseries-widget
 *      timeseries=""
 *      options=""
 *  >
 * </timeseries-widget>
 */

interface ITableOption {
    current_mode: string;
    available_modes: Array<string>;
}
interface ICellOptions { // TODO

}
interface ICellData {
    value: any;
    valueType: string,
    meta: string;
    //options: ICellOptions;
}
interface ICellMeta {
    value: any;
    meta: string;
    //options: ICellOptions;
}
interface IRow {
    head: Array<ICellMeta>;
    cells: Array<ICellData>; //[id: string]: ITableCell
    options: Object; // TODO interface
}

@Component({
    moduleId: module.id,
    selector: 'timeseries-widget',
    directives: [],
    template: `
<table class="table table-striped">
    <thead>
        <tr>
            <th *ngFor="let col of _cols">
            {{ col }}
            </th>
        </tr>
    </thead>
    <tbody>
        <tr *ngFor="let row of _rows">
            <td *ngFor="let cell of row">
                {{ cell.value }}
            </td>
        </tr>
    </tbody>
</table>
    `
})
export class TimeseriesWidgetComponent {
    private _cols: Array<string>;
    private _rows: Array<any>; //
    @Input() timeseries: Array<IRow>;
    @Input() options: ITableOption;


    constructor(private elementRef: ElementRef) { }

    ngOnChanges(c) {
        if ('timeseries' in c) {
            this._cols = [];
            this._rows = [];
            let ts = c.timeseries.currentValue;

            if (_.isArray(ts) && ts.length > 0) {
                let _c = [];
                // Fetch All Rows
                for (let i = 0; i < ts.length; i++) {
                    let row = ts[i];
                    let _row = [];
                    // Fetch head cells
                    // WARNING! Rely on sync of values of different rows
                    if (_.isArray(row.head)) {
                        for (let j = 0; j < row.head.length; j++) {
                            let cell = row.head[j];

                            if (!this._cols.length) {
                                _c.push(cell.meta);
                            }

                            _row.push(cell); ////
                        }
                    }
                    if (_.isArray(row.cells)) {
                        for (let j = 0; j < row.cells.length; j++) {
                            let cell = row.cells[j];

                            if (!this._cols.length) {
                                _c.push(cell.meta);
                            }

                            _row.push(cell); ////
                        }
                    }
                    if (_row.length > 0) {
                        this._rows.push(_row);
                    }
                    if (_c.length > 0) {
                        this._cols = _c;
                    }
                }
            } else { }
        }
    }

    ngOnInit() {
        console.log('ngOnInit')
    }

}
