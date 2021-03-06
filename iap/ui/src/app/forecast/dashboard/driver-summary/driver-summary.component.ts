import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "../data-manager.service";
import {ButtonsGroupDataInput} from "../../../common/cmp/buttons-group/buttons-group.component";
import {DecompositionTypeData, ClickableTable} from "../interfaces";

@Component({
    templateUrl: './driver-summary.component.html',
    styleUrls: ['./driver-summary.component.css']
})
export class DriverSummaryComponent implements OnInit {

    private tableData: ClickableTable = null;

    private selTableRowId: string = null;

    private decompData: {
        timescale: string;
        start: string;
        end: string;
        mid: string;
        type: string;
    } = null;

    private dTypesSwitcherData: ButtonsGroupDataInput = null;

    private dTypeData: DecompositionTypeData = null;

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
        if (this.dm.dataIsResolved) {
            this.collectData();
        } else {
            let initSubject = this.dm.init();
            initSubject.subscribe(() => {
                this.collectData();
                initSubject.complete();
            });
        }
    }

    /**
     * Collects all variables to draw Drivers Summary tab
     */
    private collectData() {
        // TODO Question about default selection

        let period = this.dm.getPeriod('main');
        let start = period.start;
        let end = period.end;
        let mid = period.mid;
        let timescale = period.timescale;

        this.selTableRowId = 'cagr/'+start+'/'+mid; // Default choice

        this.decompData = {
            timescale: timescale,
            start: start,
            end: end,
            mid: mid,
            type: this.dm.state.get('decomp_value_volume_price')
        };
        this.tableData = this.dm.getData_DriverSummaryTableData(
            start, end, mid, timescale, this.selTableRowId
        );
        this.rebuildDecompositionChart();

        this.dTypesSwitcherData = this.getDecompositionTypes();

    }


    /*-----------TABLE-SECTION--------------*/
    private onClickTableToggleButton() {
        let newStatus = (this.dm.state.get('d_summary_table_collapsed_expanded') == 'collapsed')
            ? 'expanded' : 'collapsed';
        if (newStatus == 'expanded') {
            this.tableData = this.dm.getData_DriverSummaryTableData(
                this.decompData.start,
                this.decompData.end,
                this.decompData.mid,
                this.decompData.timescale,
                this.selTableRowId
            );
        }
        this.dm.state.set('d_summary_table_collapsed_expanded', newStatus);
    }
    private onRowSelect(o) {
        let period = this.tableData.rows_data[o['row_id']];
        if (period) {
            this.selTableRowId = o['row_id'];
            this.rebuildDecompositionChart();
        } else {
            console.error('There is no id for selected row');
        }
    }
    /*-----------.TABLE-SECTION--------------*/



    /*-----------DECOMPOSITION--------------*/
    private getDecompositionTypes(): ButtonsGroupDataInput {
        // TODO Question - What type of decomposition for drivers summary
        // TODO Question - What period

        let output = [];
        let autoSel = true,
            sel;
        let types = this.dm.dataModel.getDecompositionTypes();

        for (let i = 0; i < types.length; i++) {
            if (this.dm.state.get('decomp_value_volume_price') == types[i]) {
                sel = true;
                autoSel = false;
            } else {
                sel = false;
            }
            let opt = {
                'id': types[i],
                'name': types[i],
                'selected': sel
            };
            output.push(opt);
        }
        if (autoSel && output.length > 0) {
            output[0]['selected'] = true;
        }

        return output;
    }
    private onChangedDecompType(changes: Object): void {
        this.dm.state.set('decomp_value_volume_price', changes['id']);
        this.decompData['type'] = changes['id'];
        this.rebuildDecompositionChart();
    }
    private rebuildDecompositionChart(): void {
        let selRowPeriod = this.tableData.rows_data[this.selTableRowId];
        let timescale = this.decompData['timescale'],
            type = this.decompData['type'],
            start = selRowPeriod['start'],
            end = selRowPeriod['end'];

        this.dm.getDecompositionDataAsync(type, timescale, start, end)
            .subscribe((data) => {
                this.dTypeData = data;
            });
    }
    /*-----------.DECOMPOSITION--------------*/
}
