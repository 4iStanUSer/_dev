import { Component } from '@angular/core';
import { DataService } from '../data.service'

import { SimulatorService } from '../simulator.service';


@Component({
    templateUrl: './forecast-results.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService]
})
export class ForecastResultsComponent {

    constructor(private data_manager:DataService){
        this.data_manager.getSimulatorData();

    }

}


