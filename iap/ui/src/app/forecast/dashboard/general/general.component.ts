import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "./../data-manager.service";
import {forecastValueRateData} from './data';

import {ButtonsGroupDataInput} from "./../../../common/cmp/buttons-group/buttons-group.component";
import {VariableModel} from "../../../common/model/variables.model";
import {TimelabelInput} from "../../../common/model/time-labels.model";
import {TimePeriodInput} from "../../../common/model/time-period.model";
import {DecompositionTypeData, VariableData} from "../interfaces";


type ForecastTabsAbsData = Array<{
    variable: VariableModel,
    preview: Array<VariableData>,
    full: Array<VariableData>,
}>;

@Component({
    templateUrl: './general.component.html',
    styleUrls: ['./general.component.css']
})
export class GeneralComponent implements OnInit {

    /**
     * Data for Absolute|GrowthRate switcher
     * @type {ButtonsGroupDataInput}
     */
    private absRateSwitcherData: ButtonsGroupDataInput = null;

    /**
     * Index of selected tab in Forecasting section
     * Array of tabs: tabs this.fTabsAbsData | this.fTabsRateData
     * @type {number}
     */
    private fActiveTabIndex: number = null;

    /**
     * Contains Absolute data for Bar Charts in Forecasting section
     * @type {ForecastTabsAbsData}
     */
    private fTabsAbsData: ForecastTabsAbsData = [];

    /**
     * Contains Growth Rates for Donuts in Forecasting section
     * @type {Array}
     */
    private fTabsRateData: Array<{
        variable: VariableModel,
        // TODO Create structure
    }> = [];

    /**
     * Contains available time points & current selection
     * in Forecasting section
     * @type {{data: Array<TimelabelInput>, selected: TimePeriodInput}}
     */
    private fPeriodSelectorData: { // TODO Make Interface|Type for period selector
        data: Array<TimelabelInput>,
        selected: TimePeriodInput
    } = null;

    /**
     * Contains available time points & current selection
     * in Decomposition section
     * @type {{data: Array<TimelabelInput>, selected: TimePeriodInput}}
     */
    private dPeriodSelectorData: {
        data: Array<TimelabelInput>,
        selected: TimePeriodInput
    } = null;

    /**
     * Data for decomposition type switcher
     * @type {ButtonsGroupDataInput}
     */
    private dTypesSwitcherData: ButtonsGroupDataInput = null;

    /**
     * Data for drawing WaterFall by selected type
     * @type {DecompositionTypeData}
     */
    private dTypeData: DecompositionTypeData = null;

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
        if (this.dm.dataIsResolved) {
            this.collectData();
        } else {
            let initSubject = this.dm.init();
            initSubject.subscribe(() => {
                this.collectData();
                initSubject.complete();
            });
        }
    }

    /**
     * Collects all variables to draw Dashboard tab
     */
    private collectData() {
        this.absRateSwitcherData = this.getAbsRateSwitcherData();
        this.fActiveTabIndex = this.getForecastActiveTabIndex();

        this.fTabsAbsData = this.getForecastTabsAbsData();
        this.fTabsRateData = this.getForecastTabsRateData();
        this.fPeriodSelectorData = this.getMainPeriodSelectorData();

        this.dPeriodSelectorData = this.getDecompPeriodSelectorData();
        this.dTypesSwitcherData = this.getDecompositionTypes();
        this.dTypeData = this.getDecompositionData();
    }


    private getAbsRateSwitcherData(): ButtonsGroupDataInput {
        let output = [];
        let name, sel;
        for (let i = 0; i < forecastValueRateData.length; i++) {
            name = (forecastValueRateData[i]['id'] == 'absolute')
                ? this.dm.lang['value'] : this.dm.lang['growth_rate'];
            sel = (this.dm.state.get('forecast_absolute_rate')
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
    private onChangedAbsRateState(changes: Object): void {
        this.dm.state.set('forecast_absolute_rate', changes['id']);
    }


    /*-----------FORECAST--------------*/

    private getMainPeriodSelectorData() {
        let timelabels = this.dm.getData_ForecastTimelabels();
        let period = this.dm.getPeriod('main');
        if (period) {
            let selected = {
                scale: period.timescale,
                start: period.start,
                end: period.end,
                mid: period.mid
            };
            return {
                data: timelabels,
                selected: selected
            };
        }
    }
    private getForecastTabsAbsData() {
        let output = [];
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        let period = this.dm.getPeriod('main');
        if (period) {
            let timescale = period.timescale;
            let shortList = [period.start, period.mid, period.end];
            let longList = this.dm.getFullPeriod(timescale,
                period.start, period.end);

            for (let i = 0; i < outputVars.length; i++) {
                output.push({
                    'variable': outputVars[i],
                    'preview': this.dm.getVariableData(timescale,
                        shortList, outputVars[i].key),
                    'full': this.dm.getVariableData(timescale,
                        longList, outputVars[i].key, period),
                });
            }
        }
        return output;
    }
    private getForecastTabsRateData() {
        let output = [];
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        let period = this.dm.getPeriod('main');
        if (period) {
            let timescale = period.timescale;
            let shortList = [period.start, period.mid, period.end];
            let longList = this.dm.getFullPeriod(timescale,
                period.start, period.end);

            for (let i = 0; i < outputVars.length; i++) {
                output.push({
                    'variable': outputVars[i],
                    // 'preview': this.dm.getData_ForecastRateValues(timescale, shortPeriod, outputVars[i].key),
                    // 'full': this.dm.getData_ForecastRateValues(timescale, longPeriod, outputVars[i].key),
                });
            }
        }

        return output;
    }
    private getForecastActiveTabIndex() {
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        for (let i =0;i<outputVars.length;i++) {
            if (outputVars[i].key == this.dm.state.get('forecast_active_tab')) {
                return i;
            }
        }
        return null;
    }
    private onClickForecastTab(tabName: string) {
        this.dm.state.set('forecast_active_tab', tabName);
        this.fActiveTabIndex = this.getForecastActiveTabIndex();
    }
    private onClickForecastToggleButton() {
        let now = this.dm.state.get('forecast_collapse_expand');
        let newState = (now == 'collapse') ? 'expand' : 'collapse';
        this.dm.state.set('forecast_collapse_expand', newState);
    }
    private onChangedForecastPeriod(period) {
        console.log(period);
        this.dm.setPeriod('main', period['scale'], period['start'],
            period['end'], period['mid']);

        this.fTabsAbsData = this.getForecastTabsAbsData();
        this.fTabsRateData = this.getForecastTabsRateData();

    }

    /*-----------.FORECAST--------------*/



    /*-----------DECOMPOSITION--------------*/

    private getDecompPeriodSelectorData() {
        let timelabels = this.dm.getDecompPeriodLabels();

        // TODO Check dates for existing
        let period = this.dm.getPeriod('decomp');
        if (period) {
            let selected = {
                start: period.start,
                end: period.end,
                scale: period.timescale
            };
            return {
                data: timelabels,
                selected: selected
            };
        }
    }
    private getDecompositionData() {
        let period = this.dm.getPeriod('decomp');
        if (period) {
            let type = this.dm.state.get('decomp_value_volume_price');
            return this.dm.getDecompositionData(type, period.timescale,
                period.start, period.end);
        }
    }
    private getDecompositionTypes(): ButtonsGroupDataInput {
        let defVal = this.dm.state.get('decomp_value_volume_price');
        return this.dm.getDecompTypesSwitcherData(defVal);
    }
    private onChangedDecompType(changes: Object): void {
        this.dm.state.set('decomp_value_volume_price', changes['id']);
        this.dTypeData = this.getDecompositionData();
    }
    private onChangedDecompPeriod(period) {
        this.dm.setPeriod('decomp', period['scale'], period['start'],
            period['end']);
        this.dTypeData = this.getDecompositionData();
    }

    /*-----------.DECOMPOSITION--------------*/


}
