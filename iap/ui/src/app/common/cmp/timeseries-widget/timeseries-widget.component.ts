import { Component, Input, ViewChildren, ElementRef, HostListener,
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
interface ICellProperties { // TODO
    isEditable: boolean;
    isDisabled: boolean;
}
interface ICellData {
    value: any;
    meta: string;

    valueType: string;
    props: ICellProperties;
}
interface ICellMeta {
    value: any;
    meta: string;
    //options: ICellOptions;
}


interface ICell {
    value: any;
    meta: string;
    valueType: string;
    props: ICellProperties;

}


interface IRow {
    head: Array<ICellMeta>;
    cells: Array<ICellData>; //[id: string]: ITableCell
    options: Object; // TODO interface
}

@Component({
    selector: 'timeseries-widget',
    templateUrl: 'timeseries-widget.component.html'
})
export class TimeseriesWidgetComponent {

    private _cols: Array<string>;

    private _rows: Array<any>;

    private _nowInEditMode: Array<number> = [];

    private storage: Array<any> = []; // Maybe move to external object

    // @Input() timeseries: Array<IRow>;
    // @Input() options: ITableOption;

    @ViewChildren('field_for_edit') editingFields;

    ngAfterViewChecked() {
        let editingFields = this.editingFields.toArray();
        if (editingFields.length == 1) {
            editingFields[0].nativeElement.focus();
        }
    }

    @HostListener('dblclick', ['$event']) onClick(e) {
        e.preventDefault();
        // Get TD HTML Element
        let td_el = null;
        let not_foundable = false;
        let tmp_el = e.target;
        while (!not_foundable && !td_el) {
            if (tmp_el['tagName'] == "TD") {
                td_el = tmp_el;
            } else if (tmp_el['parentElement']) {
                if (tmp_el['parentElement']['tagName'] == 'TR'
                    || tmp_el['parentElement']['tagName'] == 'TABLE') {
                    not_foundable = true;
                } else {
                    tmp_el = tmp_el['parentElement'];
                }
            } else {
                not_foundable = true;
            }
        }

        if (td_el !== null) {
            if ('dataset' in td_el && 'cell_id' in td_el['dataset']) {
                let id = td_el['dataset']['cell_id'];

                if (id && this.storage[id]) {
                    let tmpInx: number = null;
                    for (let i=0; i<this._nowInEditMode.length; i++) {
                        tmpInx = this._nowInEditMode[i];
                        if (tmpInx && this.storage[tmpInx] && tmpInx != id) {
                            this.storage[tmpInx]['status']['mode'] = 'view';
                        }
                    }
                    this._nowInEditMode = [];
                    if (this.storage[id]['props']['is_editable']) {
                        this.storage[id]['status']['mode'] = 'edit';
                    }
                    this.storage[id]['td'] = td_el; //
                    this._nowInEditMode.push(id);
                }
            }
        }
    }

    public _onInputKeyup(cell_id: number, e: Event) {
        console.log(e);
        let keyCode = e['keyCode'];
        let id = cell_id;
        if (keyCode && keyCode == 13 && id && this.storage[id]) {
            this.storage[id]['status']['mode'] = 'view';
        }
    }

    // public _onDblClick(cell_id: number, e: Event) {
    //     e.preventDefault();
    //     let id: number = cell_id;
    //     if (id && this.storage[id]) {
    //         let tmpInx: number = null;
    //         for (let i=0; i<this._nowInEditMode.length; i++) {
    //             tmpInx = this._nowInEditMode[i];
    //             if (tmpInx && this.storage[tmpInx] && tmpInx != id) {
    //                 this.storage[tmpInx]['status']['mode'] = 'view';
    //             }
    //         }
    //         this._nowInEditMode = [];
    //         this.storage[id]['status']['mode'] = 'edit';
    //         this._nowInEditMode.push(id);
    //     }
    // }

    @Input() set timeseries(timeseries: Array<IRow>) {
        console.info('TimeseriesWidgetComponent: set timeseries');
        this._cols = [];
        this._rows = [];
        let ts = timeseries;

        this.storage = [];

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

                        // _row.push(cell); ////
                        this.storage.push({
                            'meta': cell.meta,
                            'value': cell.value,
                            'valueType': 'string',
                            'props': {
                                'isEditable': false,
                                'isDisabled': true
                            },
                            'status': {
                                'mode': 'view',
                            }
                        });
                        _row.push(this.storage.length - 1);
                    }
                }
                if (_.isArray(row.cells)) {
                    for (let j = 0; j < row.cells.length; j++) {
                        let cell = row.cells[j];

                        if (!this._cols.length) {
                            _c.push(cell.meta);
                        }

                        // _row.push(cell);
                        this.storage.push({
                            'meta': cell.meta,
                            'value': cell.value,
                            'valueType': cell.valueType,
                            'props': cell.props,
                            'status': {
                                'mode': 'view',
                            }
                        });
                        _row.push(this.storage.length - 1);
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
    };

    constructor(private elRef: ElementRef) { }


}
