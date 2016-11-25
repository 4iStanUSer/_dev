import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "../data-manager.service";
import {ButtonsGroupDataInput} from "../../../common/cmp/buttons-group/buttons-group.component";
import {VariableData, ClickableTable} from "../interfaces";


interface SingleSelector {
    options: Array<{
        id: string;
        name: string;
    }>;
    selected: string;
}


@Component({
    templateUrl: './driver-detail.component.html',
    styleUrls: ['./driver-detail.component.css']
})
export class DriverDetailComponent implements OnInit {

    dTypesSwitcherData: ButtonsGroupDataInput = null;

    /**
     *
     * @type {SingleSelector}
     */
    megaDriversSelectorData: SingleSelector = null;

    tableData: ClickableTable = null;

    selectedDriver: string = null;

    dynamicData: VariableData = null;

    imapactData: VariableData = null;

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
     * Collects all variables to draw Driver's Details tab
     */
    private collectData() {
        // Order is important - maybe remake - do with subscribers
        this.dTypesSwitcherData = this.getDecompositionTypes();
        this.megaDriversSelectorData = this.getMegaDriversSelectorData();
        this.tableData = this.getTableData();
        this.dynamicData = this.getDynamicData();

        this.imapactData = this.getImapactData();
    }


    /*-----------TABLE-SECTION--------------*/
    private getDecompositionTypes(): ButtonsGroupDataInput {
        // TODO Question about default value
        let dType = this.dm.state.get('decomp_value_volume_price');
        return this.dm.getDecompTypesSwitcherData(dType);
    }

    private getMegaDriversSelectorData(): SingleSelector {
        // Get All MegaDrivers list/options
        let dType = this.dm.state.get('decomp_value_volume_price');
        let options = this.dm.getFactorsList(dType);
        if (options && options.length) {
            let selectedDrv = this.dm.state.get('d_details_selected_factor');
            if (selectedDrv && selectedDrv.length) {
                let l = options.length;
                let found: boolean = false;
                for (let i = 0; i < l; i++) {
                    if (options[i].id == selectedDrv) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    selectedDrv = options[0].id;
                }
            } else {
                selectedDrv = options[0].id;
            }
            this.dm.state.set('d_details_selected_factor', selectedDrv);
            return {
                options: options,
                selected: selectedDrv
            }
        } else {
            return null;
        }
    }

    private getTableData(): ClickableTable { //dType: string, megaDrv: string
        let dType = this.dm.state.get('decomp_value_volume_price'),
            factorId = this.dm.state.get('d_details_selected_factor');

        // Get drivers
        let drivers = this.dm.getDriversForFactor(dType, factorId);

        if (!(drivers && drivers.length)) return null;

        // Get timeperiod
        // TODO Question about this period
        let period = this.dm.getPeriod('main');

        if (!period) return null;

        // Get timelabels for the period
        // TODO Question about timescales here
        let timePoints = this.dm.getFullPeriod(period.timescale,
            period.start, period.end);

        if (!(timePoints && timePoints.length)) return null;

        let rows = [],
            cols = [],
            vals = {},
            rowsData = {},
            l: number;

        // For ROWS
        l = drivers.length;
        for (let i = 0; i < l; i++) {
            // Get Driver
            let driver = this.dm.dataModel.getVariable(drivers[i]);

            rows.push({
                id: driver.id,
                parent_id: null, // Maybe change in future
                meta: [
                    {name: driver.full_name}
                ],
                notSelectable: false
            });

            vals[driver.id] = {};
            rowsData[driver.id] = {
                driver_key: driver.id
            };
        }

        // For COLS
        l = timePoints.length;
        for (let i = 0; i < l; i++) {
            let timePoint = timePoints[i];
            // Get full timelabel - TODO

            cols.push({
                id: timePoint,
                parent_id: null, // TODO - Add real parent (IF necessary)
                meta: [
                    {name: timePoint}
                ],
                notSelectable: false
            });
        }

        // Add CAGRs COLS
        let cagrsIds = [
            'cagr/' + period.start + '/' + period.mid,
            'cagr/' + period.mid + '/' + period.end
        ];
        cols.push({
            id: cagrsIds[0],
            parent_id: null,
            meta: [
                {
                    name: this.dm.config['cagr'] + ' ' + period.start +
                        '/' + period.mid
                }
            ]
        });
        cols.push({
            id: cagrsIds[1],
            parent_id: null,
            meta: [
                {
                    name: this.dm.config['cagr'] + ' ' + period.mid +
                        '/' + period.end
                }
            ]
        });

        // Get Values
        // TODO - Add using of all timescales (Maybe!!!)
        let timeline = timePoints; // Maybe another variable
        let timescale = period.timescale;
        for (let i = 0; i < drivers.length; i++) {
            let values = this.dm.dataModel.getPointsValue(
                timescale, drivers[i], timeline);
            for (let j = 0; j < timeline.length; j++) {
                vals[drivers[i]][timeline[j]] = values[j];
            }
            // if (values && values.length) {
            //     for (let j = 0; j < values.length; j++) {
            //         vals[drivers[i]][values[j].timestamp] = values[j].value;
            //     }
            // }
            vals[drivers[i]][cagrsIds[0]] = this.dm.dataModel.getGrowthRate(
                drivers[i], period.start, period.mid, timescale);
            vals[drivers[i]][cagrsIds[1]] = this.dm.dataModel.getGrowthRate(
                drivers[i], period.mid, period.end, timescale);
        }

        this.selectedDriver = rows[0].id;

        return {
            data: {
                selected_row_id: this.selectedDriver,
                appendix: [
                    <string>this.dm.config['fact']
                ],
                cols: cols,
                rows: rows,
                values: vals
            },
            rows_data: rowsData
        }
    }
    private onChangedDecompType(changes: Object): void {
        this.dm.state.set('decomp_value_volume_price', changes['id']);

        // QUEUE
        this.dTypesSwitcherData = this.getDecompositionTypes();
        this.megaDriversSelectorData = this.getMegaDriversSelectorData();
        this.tableData = this.getTableData();
        this.dynamicData = this.getDynamicData();
        this.imapactData = this.getImapactData();
    }
    private onChangeMegaDriver(newValue: string) {
        this.dm.state.set('d_details_selected_factor', newValue);

        // QUEUE
        this.megaDriversSelectorData = this.getMegaDriversSelectorData();
        this.tableData = this.getTableData();
        this.dynamicData = this.getDynamicData();
        this.imapactData = this.getImapactData();
    }
    private onClickTableToggleButton(e: MouseEvent) {
        e.preventDefault();
        let newStatus = (this.dm.state.get('d_details_table_collapsed_expanded') == 'collapsed')
            ? 'expanded' : 'collapsed';
        this.dm.state.set('d_details_table_collapsed_expanded', newStatus);
    }

    private onRowSelect(o) {
        if (this.tableData.rows_data
            && o['row_id'] in this.tableData.rows_data) {
            this.selectedDriver =
                this.tableData.rows_data[o['row_id']].driver_key;
        } else {
            this.selectedDriver = null;
            console.error('There is no such id for selected row', o['row_id']);
        }

        this.dynamicData = this.getDynamicData();
        this.imapactData = this.getImapactData()
    }

    /*-----------.TABLE-SECTION--------------*/


    /*-----------CHARTS-SECTION--------------*/
    private getDynamicData(): VariableData {
        // Get timeperiod
        // TODO Question about this period
        let period = this.dm.getPeriod('main');
        let driverKey = this.selectedDriver;

        if (!period || !driverKey) return null;

        let timePoints = this.dm.getFullPeriod(period.timescale,
            period.start, period.end);

        if (!timePoints || timePoints.length == 0) return null;

        let driverData = this.dm.getVariableData(
            period.timescale, timePoints, driverKey, period);

        return (driverData) ? driverData : null;
    }

    private getImapactData(): VariableData {
        let period = this.dm.getPeriod('main');
        let driverKey = this.selectedDriver;
        let pss = this.dm.dataModel.getRelatedFactor(
            this.megaDriversSelectorData.selected, this.selectedDriver);
        driverKey = pss;

        console.log(this.selectedDriver);
        console.log(this.megaDriversSelectorData.selected);
        console.log(pss);


        if (!period || !driverKey) return null;

        let timePoints = this.dm.getFullPeriod(period.timescale,
            period.start, period.end);

        if (!timePoints || timePoints.length == 0) return null;

        let driverData = this.dm.getVariableData(
            period.timescale, timePoints, driverKey, period);

        return (driverData) ? driverData : null;
        /*return {
            abs: null, //BarChartDataInput;
            rate: [], //Array<number>;
            cagr: [
                {
                    start: '',
                    end: '',
                    value: null
                }
            ]
        };*/
    }

    /*-----------.CHARTS-SECTION--------------*/

}
