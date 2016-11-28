import {Component, OnInit} from '@angular/core';

import {Subject} from 'rxjs/Subject';

import {DataManagerService} from "./../data-manager.service";
import {forecastValueRateData} from './../data';

import {ButtonsGroupDataInput} from "./../../../common/cmp/buttons-group/buttons-group.component";
import {DecompositionTypeData, VariableData} from "../interfaces";
import {
    TimeSelectorDataInput,
    TimeSelectorSelectedData
} from "../../../common/cmp/time-selector/time-selector.component";
import {Variable} from "../data.model";


type ForecastTabsAbsData = Array<{
    variable: Variable,
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
     * Contains available time points & current selection
     * in Forecasting section
     * @type {{data: Array<TimelabelInput>, selected: TimePeriodInput}}
     */
    private fPeriodSelectorData: { // TODO Make Interface|Type for period selector
        data: TimeSelectorDataInput,
        selected: TimeSelectorSelectedData,
        static: Object
    } = null;

    /**
     * Contains available time points & current selection
     * in Decomposition section
     * @type {{data: Array<TimelabelInput>, selected: TimePeriodInput}}
     */
    private dPeriodSelectorData: {
        data: TimeSelectorDataInput,
        selected: TimeSelectorSelectedData,
        static: Object
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

        let forecastObj = this.getForecastTabsAbsData();
        if (forecastObj) {
            forecastObj.subscribe((d) => { this.fTabsAbsData = d; });
        }
        this.fPeriodSelectorData = this.getMainPeriodSelectorData();

        this.dPeriodSelectorData = this.getDecompPeriodSelectorData();
        this.dTypesSwitcherData = this.getDecompositionTypes();
        let decompObs = this.getDecompositionData();
        if (decompObs) {
            decompObs.subscribe((d) => { this.dTypeData = d});
        }
    }


    private getAbsRateSwitcherData(): ButtonsGroupDataInput {
        let output = [];
        let name, sel;
        for (let i = 0; i < forecastValueRateData.length; i++) {
            name = (forecastValueRateData[i]['id'] == 'absolute')
                ? this.dm.config['value'] : this.dm.config['growth_rate'];
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
                selected: selected,
                static: this.dm.getLanguagePackForTimeSelector()
            };
        }
    }
    private getForecastTabsAbsData(): Subject<ForecastTabsAbsData> {
        let subject = new Subject();

        let outputVars = this.dm.dataModel.getVariablesByType('output');
        let period = this.dm.getPeriod('main');
        if (period) {
            let timescale = period.timescale;
            let shortList = [period.start, period.mid, period.end];
            let longList = this.dm.getFullPeriod(timescale,
                period.start, period.end);

            let neededPeriods = [];
            if (shortList) {
                for (let i = 0; i < shortList.length - 1; i++) {
                    neededPeriods.push({
                        start: shortList[i],
                        end: shortList[i+1]
                    });
                }
            }
            if (longList) {
                for (let i = 0; i < longList.length - 1; i++) {
                    neededPeriods.push({
                        start: longList[i],
                        end: longList[i+1]
                    });
                }
            }

            if (neededPeriods.length) {
                let periodsToLoad = [];
                for (let i = 0; i<neededPeriods.length;i++) {
                    if (
                        !this.dm.dataModel
                            .hasChangesOverPeriod(timescale,
                                neededPeriods[i].start,
                                neededPeriods[i].end)
                    ) {
                        periodsToLoad.push(neededPeriods[i]);
                    }
                }
                if (periodsToLoad.length > 0) {
                    this.dm.loadChangesOverPeriod(timescale, periodsToLoad)
                        .subscribe(
                            (d) => {
                                let output = [];
                                for (let i = 0; i < outputVars.length; i++) {
                                    output.push({
                                        'variable': outputVars[i],
                                        'preview': this.dm.getVariableData(
                                            timescale,
                                            shortList,
                                            outputVars[i].id),
                                        'full': this.dm.getVariableData(
                                            timescale,
                                            longList,
                                            outputVars[i].id,
                                            period),
                                    });
                                }
                                subject.next(output);
                            }
                        ); // TODO Add handler for error
                } else {
                    setTimeout(() => {
                        let output = [];
                        for (let i = 0; i < outputVars.length; i++) {
                            output.push({
                                'variable': outputVars[i],
                                'preview': this.dm.getVariableData(timescale,
                                    shortList, outputVars[i].id),
                                'full': this.dm.getVariableData(timescale,
                                    longList, outputVars[i].id, period),
                            });
                        }
                        subject.next(output);
                    }, 10);
                }
            } else {
                setTimeout(() => {
                    subject.next(null);
                }, 10);
            }
        } else {
            setTimeout(() => {
                subject.next(null);
            }, 10);
        }
        return subject;



        // let output = [];
        // let outputVars = this.dm.dataModel.getVariablesByType('output');
        //
        // let period = this.dm.getPeriod('main');
        // if (period) {
        //     let timescale = period.timescale;
        //     let shortList = [period.start, period.mid, period.end];
        //     let longList = this.dm.getFullPeriod(timescale,
        //         period.start, period.end);
        //
        //     for (let i = 0; i < outputVars.length; i++) {
        //         output.push({
        //             'variable': outputVars[i],
        //             'preview': this.dm.getVariableData(timescale,
        //                 shortList, outputVars[i].id), // TODO Update to use dm.getVariableDataAsync()
        //             'full': this.dm.getVariableData(timescale,
        //                 longList, outputVars[i].id, period), // TODO Update to use dm.getVariableDataAsync()
        //         });
        //     }
        // }
        // return output;
    }
    private getForecastActiveTabIndex() {
        let outputVars = this.dm.dataModel.getVariablesByType('output');

        for (let i =0;i<outputVars.length;i++) {
            if (outputVars[i].id == this.dm.state.get('forecast_active_tab')) {
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
        this.dm.setPeriod('main', period['scale'], period['start'],
            period['end'], period['mid']);

        let forecastObj = this.getForecastTabsAbsData();
        if (forecastObj) {
            forecastObj.subscribe((d) => { this.fTabsAbsData = d; });
        }

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
                selected: selected,
                static: this.dm.getLanguagePackForTimeSelector()
            };
        }
    }
    private getDecompositionData(): Subject<DecompositionTypeData>  {
        let period = this.dm.getPeriod('decomp');
        if (period) {
            let type = this.dm.state.get('decomp_value_volume_price');
            return this.dm.getDecompositionDataAsync(type, period.timescale,
                period.start, period.end);
        }
        return null;
    }
    private getDecompositionTypes(): ButtonsGroupDataInput {
        let defVal = this.dm.state.get('decomp_value_volume_price');
        return this.dm.getDecompTypesSwitcherData(defVal);
    }
    private onChangedDecompType(changes: Object): void {
        this.dm.state.set('decomp_value_volume_price', changes['id']);
        let decompObs = this.getDecompositionData();
        if (decompObs) {
            decompObs.subscribe((d) => { this.dTypeData = d});
        }
    }
    private onChangedDecompPeriod(period) {
        this.dm.setPeriod('decomp', period['scale'], period['start'],
            period['end']);
        let decompObs = this.getDecompositionData();
        if (decompObs) {
            decompObs.subscribe((d) => { this.dTypeData = d});
        }
    }

    /*-----------.DECOMPOSITION--------------*/

}
