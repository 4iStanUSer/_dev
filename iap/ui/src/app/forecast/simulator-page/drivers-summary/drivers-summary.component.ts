import {Component, OnInit } from '@angular/core';


import { SimulatorService } from '../simulator.service';


@Component({
    templateUrl: './drivers-summary.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService]
})
export class DriversSummaryComponent implements OnInit {
    ngOnInit() {
        console.log('---ngOnInit DriversSummaryComponent');
    }
}
