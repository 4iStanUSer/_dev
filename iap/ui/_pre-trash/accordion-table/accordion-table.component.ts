import {Component, OnInit, AfterViewChecked, Input, Output, ViewChildren, EventEmitter} from '@angular/core';
import {TableModel} from "../../model/table.model";


@Component({
    selector: 'accordion-table',
    templateUrl: 'accordion-table.component.html',
    styleUrls: ['accordion-table.component.css']
})
export class AccordionTableComponent implements OnInit, AfterViewChecked {

    private tableM: TableModel = null;

    private header: Array<Object> = [];
    private body: Array<Object> = [];

    private conf: Object = {
        'isEditable': false
    };

    private nowInEditMode: Array<number> = [];


    @Input() set data(d: TableModel) {

        this.tableM = new TableModel('time_points',
            d['variables'], d['timelabels'], d['data']);

        this.header = this.tableM.getHeader();
        this.body = this.tableM.getBody();
    }

    @Input() set config(c: Object) {
        if (c && c['isEditable']) {
            this.conf['isEditable'] = true;
        }
    }

    @Output() changed = new EventEmitter();

    @ViewChildren('field_for_edit') editingFields;



    constructor() {
    }

    ngOnInit() {
    }

    ngAfterViewChecked() {
        let editingFields = this.editingFields.toArray();
        if (editingFields.length == 1) {
            editingFields[0].nativeElement.focus();
        }
    }

    asInitial() {
        this.tableM.dataCellStorage.forEach((el, i) => {
            el.isChanged = false;
        });
    }

    private onInputKeyup(cell_id: number, e: Event) {
        let keyCode = e['keyCode'];
        if (keyCode == 13) { // Enter
            if (this.tableM.dataCellStorage[cell_id].save()) {
                this.changed.emit(
                    this.tableM.dataCellStorage[cell_id].getChange()
                );
            }
        } else if (keyCode == 27) { // Esc
            this.tableM.dataCellStorage[cell_id].cancel();
        }
    }

    private onDblClick(e) {
        e.preventDefault();
        if (this.conf['isEditable']) {
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
                if ('dataset' in td_el && 'cellId' in td_el['dataset']) {
                    let cellId = td_el['dataset']['cellId'];

                    for (let i=0; i<this.nowInEditMode.length; i++) {
                        let tmpInx = this.nowInEditMode[i];
                        // this.tableM.dataCellStorage[tmpInx]['editMode'] = false;
                        this.tableM.dataCellStorage[tmpInx].cancel(); // TODO Maybe save()?
                    }
                    this.nowInEditMode = [];
                    // TODO Check if editable
                    this.tableM.dataCellStorage[cellId].setEditMode();
                    this.nowInEditMode.push(cellId);
                }
            }
        }
    }

}
