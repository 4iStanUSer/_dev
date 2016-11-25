import {Component, Input, Output, EventEmitter} from '@angular/core';
import {Helper} from "../../helper";

export interface TableWidgetRowColItem {
    id: string;
    parent_id: string;
    meta: Array<{name: string;}>;
    notSelectable?: boolean;
}
export interface TableWidgetValues {
    [row_id: string]: {
        [col_id: string]: string|number|Object;
    }
}

export interface TableWidgetData {
    selected_row_id?: string;
    appendix: Array<string>;
    rows: Array<TableWidgetRowColItem>;
    cols: Array<TableWidgetRowColItem>;
    values: TableWidgetValues;
}
// interface TableWidgetConfig {
//     mode: string; // vertical|horizontal // TODO Implement
// }


class RowModel {
    depth: number = 0;
    parent: RowModel = null;
    children: Array<RowModel> = [];
    isExpanded: boolean = false;
    isHidden: boolean = false;
    notSelectable: boolean = false;

    constructor(public id: string,
                public meta: Array<Object>) {
    }

    addParent(parent: RowModel) {
        this.parent = parent;
        this.depth = this.parent.depth + 1;
        this.parent.children.push(this);
        this.isHidden = true;
    }


    public changeExpandStatus(e: MouseEvent = null) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        if (this.children && this.children.length) {
            let expandStatus = !this.isExpanded;
            this.isExpanded = expandStatus;

            this.children.forEach((child: RowModel) => {
                if (false === expandStatus) {
                    child.hideBranch();
                } else {
                    child.showBranch();
                }
            });
        }
    }
    public showBranch() {
        this.isHidden = false;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                if (this.isExpanded) {
                    child.showBranch();
                }
            });
        }
    }
    public hideBranch() {
        this.isHidden = true;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                child.hideBranch();
            });
        }
    }
}

class ColModel {
    depth: number = 0;
    parent: ColModel = null;
    children: Array<ColModel> = [];

    constructor(public id: string,
                public meta: Array<Object>) {
    }

    addParent(parent: ColModel) {
        this.parent = parent;
        this.depth = this.parent.depth + 1;
        this.parent.children.push(this);
    }

}


@Component({
    selector: 'table-widget',
    templateUrl: './table-widget.component.html',
    styleUrls: ['./table-widget.component.css']
})
export class TableWidgetComponent {

    private transpose: boolean = false;

    private colsMetaCount: number = 0;
    private rowsMetaCount: number = 0;
    private appendixIndex: number = 0;

    private rows: Array<RowModel> = [];
    private cols: Array<ColModel> = [];
    private values: Object = null;
    private appendix: Array<string> = [];
    private selectedRowId: string = null;

    @Output('row-select') rowSelect = new EventEmitter();

    @Input() set data(d: TableWidgetData) {
        console.info('TableWidgetComponent -> set data');

        let rows: Array<RowModel> = [],
            cols: Array<ColModel> = [];
        let l: number;

        this.values = d['values'];
        this.appendix = d['appendix'];
        this.appendixIndex = 0;
        this.selectedRowId = (d['selected_row_id'])
            ? d['selected_row_id'] : null;

        // ROWS
        let rowsChildParent: Object = {};
        let rowsIdIndex: Object = {};

        // Create RowModels
        l = (d['rows'] && d['rows'].length) ? d['rows'].length : 0;
        for (let i = 0; i < l; i++) {
            let row = d['rows'][i];
            if (this.rowsMetaCount < row['meta'].length) {
                this.rowsMetaCount = row['meta'].length;
            }
            let rowM = new RowModel(row['id'], row['meta']);
            if (row['notSelectable']) {
                rowM.notSelectable = true;
            }
            rows.push(rowM);
            rowsIdIndex[row['id']] = i;
            if (row['parent_id'] !== null) {
                rowsChildParent[i] = row['parent_id'];
            }
        }
        // Linking RowModels
        for (let childIndex in rowsChildParent) {
            let parentId = rowsChildParent[childIndex];
            let parentIndex = rowsIdIndex[parentId];
            rows[childIndex].addParent(rows[parentIndex]);
        }
        this.rows = [];
        this.addItems(this.rows, rows, {});

        // COLS
        let colsChildParent: Object = {};
        let colsIdIndex: Object = {};

        // Create ColModels
        l = (d['cols'] && d['cols'].length) ? d['cols'].length : 0;
        for (let i = 0; i < l; i++) {
            let col = d['cols'][i];
            if (this.colsMetaCount < col['meta'].length) {
                this.colsMetaCount = col['meta'].length;
            }
            cols.push(new ColModel(col['id'], col['meta']));
            colsIdIndex[col['id']] = i;
            if (col['parent_id'] !== null) {
                colsChildParent[i] = col['parent_id'];
            }
        }
        // Linking ColModels
        for (let childIndex in colsChildParent) {
            let parentId = colsChildParent[childIndex];
            let parentIndex = colsIdIndex[parentId];
            cols[childIndex].addParent(cols[parentIndex]);
        }
        this.cols = [];
        this.addItems(this.cols, cols, {});

    }

    constructor() {
    }

    private onClickRow(row: RowModel) {
        if (!row.notSelectable) {
            if (this.selectedRowId != row.id) {
                this.selectedRowId = row.id;
                this.rowSelect.emit({
                    row_id: row.id
                });
            }
        }
    }

    private getValue(row_id: string, col_id: string) {
        try {
            return this.values[row_id][col_id]; // TODO Add for objects
        } catch (e) {
            return null;
        }
    }

    private addItems(addInto: Array<RowModel|ColModel>,
                     addWhat: Array<RowModel|ColModel>,
                     alreadyAdded: Object) {
        for (let i=0;i<addWhat.length;i++) {
            if (!alreadyAdded[addWhat[i].id]) {
                alreadyAdded[addWhat[i].id] = true;
                addInto.push(addWhat[i]);
                if (addWhat[i].children.length) {
                    this.addItems(addInto, addWhat[i].children, alreadyAdded);
                }
            }
        }
    }

    private range(i: number) {
        return Helper.range(i);
    }
}
