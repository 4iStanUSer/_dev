import * as _ from 'lodash';
import {TblRow, RowOptions} from './interfaces';

export class RowModel {
    id: number|string = null;
    meta: Array<Object> = [];

    data: Object = {};

    children: Array<RowModel> = [];
    parent: RowModel = null;
    options: RowOptions = {};
    depth: number = 0;

    isShown: boolean = true;
    isExpanded: boolean = false;

    isHeader: boolean = false;

    constructor(id: number, tblRow: TblRow, parent: RowModel, is_header: boolean = false) {
        this.id = id;
        this.isHeader = is_header;
        this.meta = [tblRow['meta']];
        this.data = tblRow['data'];
        if (parent !== null) {
            this.depth = parent.depth + 1;
            this.isShown = false;
            this.parent = parent;
            parent.children.push(this);
        }
    }

    getData(v: string) {
        return (this.data[v]) ? this.data[v]['value'] : null;
    }

    public changeExpandStatus() {
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
        this.isShown = true;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                if (this.isExpanded) {
                    child.showBranch();
                }
            });
        }
    }
    public hideBranch() {
        this.isShown = false;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                child.hideBranch();
            });
        }
    }

}
