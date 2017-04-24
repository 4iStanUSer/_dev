import { Component } from '@angular/core';
import { DataService } from '../data.service'
import { SimulatorService } from '../simulator.service';
import {BarChartDataInput} from "../../../common/cmp/bar-chart/bar-chart.component";

@Component({
    templateUrl: './forecast-results.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService]
})
export class ForecastResultsComponent {

    /**
     * Variable contain for Bar Chart
     *
     */
    public BarChartData:BarChartDataInput=[];

    constructor(private data_manager:DataService){
        this.data_manager.getSimulatorData();
        this.BarChartData = [
            {'name':'2015', 'value':1.000},
            {'name':'2016', 'value':2.000},
            {'name':'2017', 'value':3.000},
            {'name':'2017', 'value':4.000}
        ];

    }

}


