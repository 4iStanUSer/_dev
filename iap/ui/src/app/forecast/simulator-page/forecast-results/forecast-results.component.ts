import {Component, OnInit } from '@angular/core';
import { SimulatorService } from '../simulator.service';


@Component({
    templateUrl: './forecast-results.component.html',
    providers: [SimulatorService]
})
export class ForecastResultsComponent implements OnInit {
    constructor(private __simulatorService: SimulatorService) { }

    ngOnInit() {
        console.log('---ngOnInit ForecastResultsComponent', this.__simulatorService.getData());
    }
}


