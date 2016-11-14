import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "../data-manager.service";

@Component({
    templateUrl: './driver-detail.component.html',
    styleUrls: ['./driver-detail.component.css']
})
export class DriverDetailComponent implements OnInit {

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
    }

}
