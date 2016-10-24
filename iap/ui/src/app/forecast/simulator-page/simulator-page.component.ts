import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute, Params} from '@angular/router';
import {SimulatorPageDataManagerService} from "./simulator-page-data-manager.service";

@Component({
    templateUrl: './simulator-page.component.html',
    styleUrls: ['./simulator-page.component.css']
})
export class SimulatorPageComponent implements OnInit {

    private entityId: number = null;

    private tableData: Object = null;

    constructor(private route: ActivatedRoute,
                private router: Router,
                private service: SimulatorPageDataManagerService) {
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

}
