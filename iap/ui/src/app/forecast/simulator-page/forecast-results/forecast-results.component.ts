import { Component, OnInit } from '@angular/core';


import { SimulatorService } from '../simulator.service';
import { NewSimulatorService } from '../new_simulator.service';
import { LocalStorageService } from 'angular-2-local-storage';


@Component({
    templateUrl: './forecast-results.component.html',
    styleUrls: ['./../simulator-page.component.css'],
    providers: [SimulatorService, NewSimulatorService]
})
export class ForecastResultsComponent implements OnInit {
    default_config: Object = {
        header_title_collapse: 'Forecasted Results --local',
        header_title_expand: 'Forecasted Sales --local',
        forecast_collapse_expand: 'collapse',
        forecast_collapse_button_title: 'Collapse',
        forecast_expand_button_title: 'Expand'
    };

    /**
     * Current config for page
     * @type {Object}
     */
    private config: Object = {};

    /**
     * Current state for page
     * @type {Object}
     */
    private state: Object = {};


    constructor (
        private __localStorageService: LocalStorageService,
        private __newSimulatorService: NewSimulatorService,
    ) {}


    // Load global config and merge with local config
    __getConfig(default_congig:Object) {
        return default_congig;
    }

    private __getCurrentState():void {
        this.state['forecast_collapse_expand'] = (
            this.__localStorageService.get('simulator_forecast_collapse_expand')
        ) ? this.__localStorageService.get('simulator_forecast_collapse_expand') : this.config['forecast_collapse_expand'];
        this.state['forecast_absolute_rate'] = this.__localStorageService.get('simulator_forecast_absolute_rate');
    }

    ngOnInit() {
        console.log('---ngOnInit ForecastResultsComponent');
        this.config = this.__getConfig(this.default_config);
        this.__getCurrentState();
    }

    public updateState():void  {
        this.__getCurrentState();
    }

    private onSwitcherForecastCollapseExpandButton() {
        let now = this.state['forecast_collapse_expand'];
        let newState = (now == 'collapse') ? 'expand' : 'collapse';
        this.state['forecast_collapse_expand'] = newState;
        this.__localStorageService.set('simulator_forecast_collapse_expand', newState);
    }
}


