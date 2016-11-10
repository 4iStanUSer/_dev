import {Component, OnInit} from '@angular/core';
import {DataManagerService} from "./../data-manager.service";
import {forecastValueRateData} from './data';

import {ButtonDataInput} from "./../../../common/cmp/buttons-group/buttons-group.component";
import {VariableModel} from "../../../common/model/variables.model";
import {TimelabelInput} from "../../../common/model/time-labels.model";
import {TimePeriodInput} from "../../../common/model/time-period.model";
import {WaterfallChartDataInput} from "../../../common/cmp/waterfall-chart/waterfall-chart.component";



@Component({
    templateUrl: './general.component.html',
    styleUrls: ['./general.component.css']
})
export class GeneralComponent implements OnInit {

    private locState: {[s: string]: any} = null; // TODO Implement this variable!!!

    private periods: Object = null;

    private absRateSwitcherData: Array<ButtonDataInput> = null;

    private fActiveTabIndex: number = null;

    private fTabsAbsData: Array<{
        variable: VariableModel,
        preview: Array<Object>, // TODO Replace by input interface of BarChart
        full: Array<Object>, // TODO Replace by input interface of BarChart
    }> = [];

    private fTabsRateData: Array<{
        variable: VariableModel,
        // TODO Create structure
    }> = [];

    private fPeriodSelectorData: {
        data: Array<TimelabelInput>,
        selected: TimePeriodInput
    } = null;

    private dPeriodSelectorData: {
        data: Array<TimelabelInput>,
        selected: TimePeriodInput
    } = null;

    private dTypesSwitcherData: Array<ButtonDataInput> = null;

    private dTypeData: {
        abs: WaterfallChartDataInput,
        rate: WaterfallChartDataInput,
    } = null;

    constructor(private dm: DataManagerService) {
        // console.log('GeneralComponent');
        // this.dm.isFilled.subscribe((a) => {
        //     console.log(a);
        // });
    }

    ngOnInit() {
        // TODO - Remake: double query!!!
        this.dm.getDataModel().subscribe(() => {
            this.periods = this.dm.periods; // TODO Maybe remake

            this.absRateSwitcherData = this.getAbsRateSwitcherData();
            this.fActiveTabIndex = this.getForecastActiveTabIndex();

            this.fTabsAbsData = this.getForecastTabsAbsData();
            this.fTabsRateData = this.getForecastTabsRateData();
            this.fPeriodSelectorData = this.getMainPeriodSelectorData();

            this.dPeriodSelectorData = this.getDecompPeriodSelectorData();
            this.dTypesSwitcherData = this.getDecompositionTypes();
            this.dTypeData = this.getDecompositionData();
        });
    }


    private getAbsRateSwitcherData(): Array<ButtonDataInput> {
        let output = [];
        let name, sel;
        for (let i = 0; i < forecastValueRateData.length; i++) {
            name = (forecastValueRateData[i]['id'] == 'absolute')
                ? this.dm.lang['value'] : this.dm.lang['growth_rate'];
            sel = (this.dm.state.get('forecast_absolute_rate') == forecastValueRateData[i]['id'])
                ? true : false;
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
        let selected = {
            start: '2013',
            end: '2017',
            scale: 'annual',
            mid: '2015'
        };
        return {
            data: timelabels,
            selected: selected
        };
    }
    private getForecastTabsAbsData() {
        let output = [];
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        let timescale = 'annual';
        // TODO USE this.periods
        let shortPeriod = ['2013', '2015', '2017'];
        let longPeriod = ['2013', '2014', '2015', '2016', '2017'];


        for (let i = 0; i < outputVars.length; i++) {
            output.push({
                'variable': outputVars[i],
                'preview': this.dm.getData_ForecastAbsValues(timescale, shortPeriod, outputVars[i].key),
                'full': this.dm.getData_ForecastAbsValues(timescale, longPeriod, outputVars[i].key),
            });
        }
        return output;
    }
    private getForecastTabsRateData() {
        let output = [];
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        let timescale = 'annual';
        // TODO USE this.periods
        let shortPeriod = ['2013', '2015', '2017'];
        let longPeriod = ['2013', '2014', '2015', '2016', '2017'];

        for (let i = 0; i < outputVars.length; i++) {
            output.push({
                'variable': outputVars[i],
                // 'preview': this.dm.getData_ForecastRateValues(timescale, shortPeriod, outputVars[i].key),
                // 'full': this.dm.getData_ForecastRateValues(timescale, longPeriod, outputVars[i].key),
            });
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
    private onChangedForecastPeriod(period) { //TimePeriodInput
        console.log(period);
    }

    /*-----------.FORECAST--------------*/



    /*-----------DECOMPOSITION--------------*/

    private getDecompPeriodSelectorData() {
        let timelabels = this.dm.getDecompPeriodLabels();

        // TODO Check dates for existing
        let selected = {
            start: this.periods['decomposition']['start'],
            end: this.periods['decomposition']['end'],
            scale: 'annual', // TODO Replace
        };
        return {
            data: timelabels,
            selected: selected
        };

    }
    private getDecompositionData() {
        let timescale = 'annual';
        // TODO USE PeriodsModel
        let start = this.periods['decomposition']['start'];
        let end = this.periods['decomposition']['end'];
        let type = this.dm.state.get('decomp_value_volume_price');

        return this.dm.getData_Decomposition(type, timescale, start, end);
    }
    private getDecompositionTypes(): Array<ButtonDataInput> {

        let output = [];
        let autoSel = true,
            sel;
        let types = this.dm.decompModel.getDecompositionTypes();

        for (let i = 0; i < types.length; i++) {
            if (this.dm.state.get('decomp_value_volume_price') == types[i]) {
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
    private onChangedDecompType(changes: Object): void {
        this.dm.state.set('decomp_value_volume_price', changes['id']);
        this.dTypeData = this.getDecompositionData();
    }
    private onChangedDecompPeriod(period) {
        console.log(period);
    }

    /*-----------.DECOMPOSITION--------------*/


}
