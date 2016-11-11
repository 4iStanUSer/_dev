import {Component, OnInit, ViewChild} from '@angular/core';
import {Router, ActivatedRoute, Params} from '@angular/router';
import {SimulatorPageDataManagerService} from "./simulator-page-data-manager.service";
// import {AccordionTableComponent} from "../../common/cmp/accordion-table/accordion-table.component";

@Component({
    templateUrl: './simulator-page.component.html',
    styleUrls: ['./simulator-page.component.css']
})
export class SimulatorPageComponent implements OnInit {

    private entityId: number = null;

    private tableData: Object = null;

    private queueToSave = [];

    @ViewChild('acc_table') accTableObj: any; //AccordionTableComponent;

    constructor(private route: ActivatedRoute,
                private router: Router,
                public service: SimulatorPageDataManagerService) {
    }

    ngOnInit() {
        this.route.params.forEach((params: Params) => {
            this.entityId = (+params['id']) ? +params['id'] : null;
            this.service.init(this.entityId)
                .subscribe((d)=> {
                    this.tableData = this.service.getData_VTable();
                });
        });
    }

    recalculate() {
        console.log('Send to server next: ');
        console.log(this.queueToSave);
        this.accTableObj.asInitial();
        this.queueToSave = [];
    }

    onTableDataChanged(change: Object) {
        let keysToCompare = Object.keys(change).filter((key)=> {
            return (key != 'value') ? true : false;
        });
        let foundIndexInQueue = this.queueToSave.findIndex((el) => {
            for (let i=0;i<keysToCompare.length; i++) {
                if (el[keysToCompare[i]] != change[keysToCompare[i]]) {
                    return false;
                }
            }
            return true;
        });
        if (foundIndexInQueue != -1) {
            this.queueToSave[foundIndexInQueue] = change;
        } else {
            this.queueToSave.push(change);
        }
    }

}
