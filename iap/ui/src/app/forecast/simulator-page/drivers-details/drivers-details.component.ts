import {Component, OnInit } from '@angular/core';


import { SimulatorService } from '../simulator.service';


@Component({
    templateUrl: './drivers-details.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService]
})
export class DriversDetailsComponent implements OnInit {
    ngOnInit() {
        console.log('---ngOnInit DriversDetailsComponent');
    }
}

