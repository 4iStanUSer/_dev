import {Component, ViewChild} from '@angular/core';


import {ForecastResultsComponent} from './forecast-results/forecast-results.component';


import {LocalStorageService} from 'angular-2-local-storage';
import {SimulatorService} from './simulator.service';
import { NewSimulatorService } from './new_simulator.service';
import {forecastValueRateData} from './../dashboard/data';


import {ButtonsGroupDataInput} from "./../../common/cmp/buttons-group/buttons-group.component";


@Component({
    templateUrl: './simulator-page.component.html',
    styleUrls: ['./simulator-page.component.css'],
    providers: [SimulatorService, NewSimulatorService]
})
export class SimulatorPageComponent {
    /**
     * Data for Absolute|GrowthRate switcher
     * @type {ButtonsGroupDataInput}
     */
    private absRateSwitcherData: ButtonsGroupDataInput = null;

    /**
     * Data for decomposition type switcher
     * @type {ButtonsGroupDataInput}
     */
    private valueVolumePriceSwitcherData: ButtonsGroupDataInput = null;

    /**
     * Data for scenarios list
     * @type {Object[]}
     */
    private scenariosList: Object[] = [];
    private baseScenario:Object = null;
    private simulationScenario:Object = null;

    simulator_data: Object = {};
    default_config: Object = {
        forecast_results_tab_name: 'Forecast Results --local',
        drivers_summary_tab_name: 'Driver\'s Summary --local',
        drivers_details_tab_name: 'Driver\'s Details --local',
        scenario_insights_tab_name: 'Scenario Insights --local',
        forecast_absolute_rate: 'absolute',
        value_title: 'Value', // ?????
        growth_rate_title: 'Growth rate', // ?????
        forecast_value_volume_price: 'value',
    };
    config: Object = null;

    @ViewChild(ForecastResultsComponent) forecastResultsComponent: ForecastResultsComponent;


    constructor(
        private __localStorageService: LocalStorageService,
        private __simulatorService: SimulatorService,
        private __newSimulatorService: NewSimulatorService,
    ) { }

    getSimulatorData(): void {
        this.__simulatorService.getSimulatorData().then(data => this.simulator_data = data);
    }

    public forecastResultsComponentUpdateState() {
        this.forecastResultsComponent.updateState();
    }

    // Load global config and merge with local config
    __getConfig(default_congig:Object) {
        return default_congig;
    }

    ngOnInit() {
        console.log('---ngOnInit Simulator Page');
        this.config = this.__getConfig(this.default_config);

        // Update localStorage
        this.__localStorageService.set('simulator_forecast_absolute_rate', this.config['forecast_absolute_rate']);
        this.__localStorageService.set('simulator_forecast_value_volume_price', this.config['forecast_value_volume_price']);
        this.__localStorageService.set('simulator_base_scenario', this.baseScenario);

        this.collectData();
    }

    private collectData() {
        this.absRateSwitcherData = this.getAbsRateSwitcherData();
        this.valueVolumePriceSwitcherData = this.getValueVolumePriceSwitcherData();


        this.scenariosList = this.__newSimulatorService.getScenariosList();
        this.baseScenario = this.__newSimulatorService.getBaselineScenario();
        this.simulationScenario = this.__newSimulatorService.getSimulationScenario();
    }

    private getAbsRateSwitcherData(): ButtonsGroupDataInput {
        let output = [];
        let name, sel;
        for (let i = 0; i < forecastValueRateData.length; i++) {
            name = (forecastValueRateData[i]['id'] == 'absolute')
                ? this.config['value_title'] : this.config['growth_rate_title'];
            sel = (this.__localStorageService.get('simulator_forecast_absolute_rate')
                    == forecastValueRateData[i]['id']) ? true : false;
            let opt = {
                'id': forecastValueRateData[i]['id'],
                'name': name,
                'selected': sel
            };
            output.push(opt);
        }
        return output;
    }

    private getValueVolumePriceSwitcherData(): ButtonsGroupDataInput {
        const defVal = this.__localStorageService.get('simulator_forecast_value_volume_price').toString();
        return this.__getDecompTypesSwitcherData(defVal);
    }

    /**
     * Returns data for Decomposition Types Switcher.
     * This data is ready to use in template
     * @param defaultVal
     * @returns {ButtonsGroupDataInput}
     */
    __getDecompTypesSwitcherData(defaultVal: string): ButtonsGroupDataInput {
        let output = [];
        let autoSel = true,
            sel;
        //let types = this.dataModel.getDecompositionTypes();
        let types = ['value','volume','price'];

        for (let i = 0; i < types.length; i++) {
            if (defaultVal == types[i]) {
                sel = true;
                autoSel = false;
            } else {
                sel = false;
            }
            let opt = {
                'id': types[i],
                'name': types[i],
                'selected': sel
            };
            output.push(opt);
        }
        if (autoSel && output.length > 0) {
            output[0]['selected'] = true;
        }
        return output;
    }

    private onChangedAbsRateState(changes: Object): void {
        console.log('---onChangedAbsRateState');
        this.__localStorageService.set('simulator_forecast_absolute_rate', changes['id']);
        this.forecastResultsComponentUpdateState();
    }

    private onChangedValueVolumePriceSwitcherData(changes: Object): void {
        console.log('---onChangedValueVolumePriceSwitcherData');
        this.__localStorageService.set('simulator_forecast_value_volume_price', changes['id']);
        this.forecastResultsComponentUpdateState();
    }

    private onChangedBaselineScenario(event:any): void {
        console.log('---onChangedBaselineScenario', event.target.value);
        this.__localStorageService.set('simulator_base_scenario', event.target.value);
        this.forecastResultsComponentUpdateState();
    }
}
