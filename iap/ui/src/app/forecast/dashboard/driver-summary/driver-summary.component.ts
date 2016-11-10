import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "../data-manager.service";
import {TableWidgetData} from "../../../common/cmp/table-widget/table-widget.component";

@Component({
    templateUrl: './driver-summary.component.html',
    styleUrls: ['./driver-summary.component.css']
})
export class DriverSummaryComponent implements OnInit {

    private tableData: TableWidgetData = null;

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
        this.tableData = this.dm.getData_DriverSummaryTable();
        console.log(this.tableData);
    }

    onRowSelect(o) {
        console.log(o);
    }

}
