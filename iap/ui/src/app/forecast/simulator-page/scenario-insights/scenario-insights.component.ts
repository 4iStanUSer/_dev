import {Component, OnInit } from '@angular/core';


import { SimulatorService } from '../simulator.service';


@Component({
    templateUrl: './scenario-insights.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService]
})
export class ScenarioInsightsComponent implements OnInit {
    ngOnInit() {
        console.log('---ngOnInit ScenarioInsightsComponent');
    }
}
