import {Component} from '@angular/core';


import {SimulatorService} from './simulator.service';


@Component({
    templateUrl: './simulator-page.component.html',
    styleUrls: ['./simulator-page.component.css'],
    providers: [SimulatorService]
})
export class SimulatorPageComponent {
    simulator_data: Object = {};

    constructor(private __simulatorService: SimulatorService) { }

    getSimulatorData(): void {
        this.__simulatorService.getSimulatorData().then(data => this.simulator_data = data);
    }
}
