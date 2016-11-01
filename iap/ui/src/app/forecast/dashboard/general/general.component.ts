import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "../data-manager.service";

@Component({
    templateUrl: './general.component.html',
    styleUrls: ['./general.component.css']
})
export class GeneralComponent implements OnInit {

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
    }

}
