import {Injectable} from '@angular/core';

import {Observable} from 'rxjs/Observable';
import {Subject} from 'rxjs/Subject';

/*======TEMP=====*/
import {
    defaultState, dashboardConfig,
    // selectorsDataTEMP, selectorsConfigTEMP,
} from './data';
/*======.TEMP=====*/


import {AjaxService} from "./../../common/service/ajax.service";
import {
    StaticDataService,
    PageState
} from "../../common/service/static-data.service";
import {InsightInput} from "./insights/insights.component";
import {
    TableWidgetRowColItem,
    TableWidgetValues
} from "../../common/cmp/table-widget/table-widget.component";

import {ButtonsGroupDataInput} from "../../common/cmp/buttons-group/buttons-group.component";
import {
    VariableData,
    ClickableTable,
    DecompositionTypeData
} from "./interfaces";
import {TimeSelectorDataInput} from "../../common/cmp/time-selector/time-selector.component";
import {DashboardDataModel} from "./data.model";

class Period {
    constructor(public timescale: string = null,
                public start: string = null,
                public end: string = null,
                public mid: string = null) {
    }
}

@Injectable()
export class DataManagerService {

    private pageName: string = 'dashboard';

    isData: Object = {
        dynamic: {
            sent: false,
            received: false,
            processed: false,
        },
        static: {
            sent: false,
            received: false,
            processed: false,
        }
    };

    dataIsResolved: boolean = false;

    dataModel: DashboardDataModel = null;

    insights: Array<InsightInput> = [];

    state: PageState = null;

    config: Object = null; // TODO Interface for config

    ddConfig: Object = null; // Dynamic Data Config

    initResolver: Subject<number> = null;

    periods: {
        main: Period,
        decomp: Period
    } = {
        main: null,
        decomp: null
    };
    // ----------------------------- //

    selectors: {data: Object, config: Object} = {data: null, config: null};

    constructor(private req: AjaxService,
                private sds: StaticDataService) { //private stateService: StateService,

        //this.init();
    }

    init() {
        if (!this.initResolver) {
            this.initResolver = new Subject();
            // this.initSelectors();
            this.initDynamicData();
            this.initStaticData();
            this.initResolver.subscribe(() => {
                //console.log('DataManager init() subscriber');
            });
        } else {
            setTimeout(() => {
                this.resolveInitObervable();
            }, 10);
        }
        return this.initResolver;
    }

    private resolveInitObervable() {
        if (this.dataInitialized()) {
            this.dataIsResolved = true;
            this.initResolver.next(2);
        }
    }

    private dataInitialized() {
        return (this.isData['dynamic']['received']
        && this.isData['static']['received']);
    }

    // private initSelectors(): void {
    //     this.req.get({
    //         url_id: 'forecast/get_entity_selectors_config',
    //         data: {}
    //     }).subscribe((data) => {
    //         this.selectors['config'] = data;
    //     });
    //
    //     this.req.get({
    //         url_id: 'forecast/get_options_for_entity_selector',
    //         data: {
    //             query: [null, null, null, null]
    //         }
    //     }).subscribe((data) => {
    //         this.selectors['data'] = data;
    //     });
    // }

    private initDynamicData(): void {
        if (this.isData['dynamic']['sent']) return;

        this.isData['dynamic']['sent'] = true;
        this.isData['dynamic']['received'] = false;

        this.req.get({
            'url_id': 'forecast/get_dashboard_data',
            'data': {
                'entities_ids': [2]
            }
        }).subscribe((data)=> {
                this.isData['dynamic']['received'] = true;

                let d = data['data'];
                let c = data['config'];

                this.ddConfig = c;

                this.insights = d['insights'];

                this.periods['main'] = new Period(
                    c['main_period']['timescale'],
                    c['main_period']['start'],
                    c['main_period']['end'],
                    c['main_period']['mid']
                );
                this.periods['decomp'] = new Period(
                    c['decomp_period']['timescale'],
                    c['decomp_period']['start'],
                    c['decomp_period']['end']
                );


                this.dataModel = new DashboardDataModel(
                    d['timescales'],
                    d['timelables'],
                    d['variables'],
                    d['variable_values'],
                    d['change_over_period'],
                    d['decomp_types'],
                    d['decomp'],
                    d['factor_drivers'],
                    d['decomp_type_factors'],
                );


                ////////////////////
                // this.selectors = {
                //     data: selectorsDataTEMP,
                //     config: selectorsConfigTEMP
                // };
                ////////////////////

                this.isData['dynamic']['processed'] = true;

                this.resolveInitObervable();
            },
            (e)=> {
                console.error('Didn\'t receive dynamic data for dashboard page!');
            });
    }

    private proceedStaticData() {
        this.isData['static']['received'] = true;

        this.config = this.sds.getConfig(this.pageName);
        this.state = this.sds.getState(this.pageName);

        this.resolveInitObervable();
    }

    private initStaticData() {
        if (this.isData['static']['sent']) return;

        this.isData['static']['sent'] = true;
        this.isData['static']['received'] = false;

        if (!this.sds.hasPage(this.pageName)) {
            let frontData = {
                'state': defaultState,
                'config': dashboardConfig
            };
            this.req.get({
                'url_id': 'forecast/get_page_static_data',
                'data': {
                    'page_name': this.pageName
                }
            }).subscribe((d)=> {
                    this.sds.addPage(this.pageName, frontData, d);
                    this.proceedStaticData();
                },
                (e)=> {
                    this.sds.addPage(this.pageName, frontData);
                    this.proceedStaticData();
                });
        } else {
            this.proceedStaticData();
        }
    }

    getPeriod(name: string): Period {
        return (this.periods[name]) ? this.periods[name] : null;
    }

    setPeriod(name: string, timescale: string, start: string,
              end: string, mid: string = null) {
        if (this.periods[name]) {
            this.periods[name].timescale = timescale;
            this.periods[name].start = start;
            this.periods[name].end = end;
            this.periods[name].mid = mid;
        }
    }

    /**
     * Returns Variable's Data: absolute values, growth rates and CAGRS
     * If cagrsPeriod is not defined - it returns data without 'cagr' key
     * @param timescale_id
     * @param timepoints_ids
     * @param variable_id
     * @param cagrsPeriod
     * @returns {VariableData}
     */
    getVariableData(timescale_id: string,
                    timepoints_ids: Array<string>,
                    variable_id: string,
                    cagrsPeriod: Period = null): VariableData {

        let pointsValue: Array<number>;
        let output: VariableData = {
            abs: [],
            rate: [],
            cagr: null
        };

        let l = (timepoints_ids && timepoints_ids.length)
            ? timepoints_ids.length : 0;

        pointsValue = this.dataModel.getPointsValue(timescale_id, variable_id,
            timepoints_ids);
        for (let i = 0; i < l; i++) {
            // timepoints[i] - TODO get full_name
            output.abs.push({
                name: timepoints_ids[i],
                value: pointsValue[i]
            });
        }
        // for (let j = 0; j < pointsValue.length; j++) {
        //     output.abs.push({
        //         name: pointsValue[j].timestamp, // OR timelabel.full_name
        //         value: pointsValue[j].value
        //     });
        // }
        for (let i = 0; i < l - 1; i++) {
            let start = timepoints_ids[i];
            let end = timepoints_ids[i + 1];
            let growth = this.dataModel.getGrowthRate(variable_id, start,
                end, timescale_id);
            output.rate.push({
                name: start + '/' + end,
                value: growth
            });
        }
        if (cagrsPeriod) {
            output.cagr = [
                {
                    start: cagrsPeriod.start,
                    end: cagrsPeriod.mid,
                    value: this.dataModel.getGrowthRate(
                        variable_id,
                        cagrsPeriod.start,
                        cagrsPeriod.mid,
                        cagrsPeriod.timescale)
                },
                {
                    start: cagrsPeriod.mid,
                    end: cagrsPeriod.end,
                    value: this.dataModel.getGrowthRate(
                        variable_id,
                        cagrsPeriod.mid,
                        cagrsPeriod.end,
                        cagrsPeriod.timescale)
                },
            ]
        }
        return output;
    }

    loadChangesOverPeriod(timescale_id: string,
                            periods: Array<{start: string, end: string}>) {
        return this.req.get({
            url_id: 'forecast/get_changes_for_period',
            data: {
                'timescale': timescale_id,
                'periods': periods
            }
        })
    }

    getVariableDataAsync(timescale_id: string,
                         timepoints_ids: Array<string>,
                         variable_id: string,
                         cagrsPeriod: Period = null): Subject<VariableData> {
        let subject = new Subject();

        let periodsToLoad = [];
        for (let i=0;i<timepoints_ids.length - 1; i++) {
            let start = timepoints_ids[i],
                end = timepoints_ids[i+1];

            if (!this.dataModel
                    .hasChangesOverPeriod(timescale_id, start, end)) {
                periodsToLoad.push({
                    start: timepoints_ids[i],
                    end: timepoints_ids[i+1],
                });
            }
        }

        if (periodsToLoad.length > 0) {
            this.req.get({
                url_id: 'forecast/get_changes_for_period',
                data: periodsToLoad
            }).subscribe(
                (data) => {
                    this.dataModel.addChangesOverPeriod(data);
                    let varData = this.getVariableData(
                        timescale_id,
                        timepoints_ids,
                        variable_id,
                        cagrsPeriod
                    );
                    subject.next(varData);
                }
            );
        } else {
            setTimeout(() => {
                let varData = this.getVariableData(
                    timescale_id,
                    timepoints_ids,
                    variable_id,
                    cagrsPeriod
                );
                subject.next(varData);
            }, 10);
        }

        return subject;
    }

    /**
     * Returns Decomposition's Data:
     * absolute values, rates and and item changes
     * @param decomp_type_id
     * @param timescale_id
     * @param start
     * @param end
     * @returns {DecompositionTypeData}
     */
    getDecompositionData(decomp_type_id: string,
                         timescale_id: string,
                         start: string,
                         end: string): DecompositionTypeData {
        let output = {
            'abs': [],
            'rate': [],
            'table': []
        };
        let decomp = this.dataModel.getDecomposition(decomp_type_id,
            timescale_id, start, end);

        let l = (decomp && decomp.factors && decomp.factors.length)
            ? decomp.factors.length : 0;
        let lastMetric = '';
        for (let i = 0; i < l; i++) {
            let factor = decomp.factors[i];
            let variable = this.dataModel.getVariable(factor.var_id);
            let factorName = (variable) ? variable.full_name : null;
            let factorMetric = (variable) ? variable.metric : null;
            if (i == 0) {
                lastMetric = factorMetric;
                output['abs'].push({
                    name: start,
                    value: factor.abs,
                    metric: factorMetric,
                });
                output['rate'].push({
                    name: start,
                    value: factor.rate,
                    metric: '%',
                });
                if (i != 0 && i != l - 1) {
                    output['table'].push({
                        name: start,
                        value: factor.rate,
                        metric: '%',
                    });
                }
            }
            else {
                output['abs'].push({
                    name: factorName,
                    value: factor.abs,
                    metric: factorMetric,
                });
                output['rate'].push({
                    name: factorName,
                    value: factor.rate,
                    metric: '%',
                });
                if (i != 0 && i != l - 1) {
                    output['table'].push({
                        name: factorName,
                        value: factor.rate,
                        metric: '%',
                    });
                }
            }
        }
        if (l > 0) {
            output['abs'].push({
                name: end,
                value: 0,
                metric: lastMetric,
            });
            output['rate'].push({
                name: end,
                value: 0,
                metric: '%',
            });
            /*if (i != 0 && i != l - 1) {
             output['table'].push({
             name: end,
             value: 0,
             metric: '%',
             });
             }*/
        }

        return output;
    }

    getDecompositionDataAsync(decomp_type_id: string,
                              timescale_id: string,
                              start: string,
                              end: string): Subject<DecompositionTypeData> {
        let subject = new Subject();

        if (!this.dataModel.hasDecomposition(timescale_id, start, end)) {
            this.req.get({
                url_id: 'forecast/get_decomposition_for_period',
                data: {
                    timescale: timescale_id,
                    start: start,
                    end: end
                }
            }).subscribe(
                (data) => {
                    this.dataModel.addDecomposition(data);
                    let decData = this.getDecompositionData(
                        decomp_type_id,
                        timescale_id,
                        start,
                        end
                    );
                    subject.next(decData);
                }
            );
        } else {
            setTimeout(() => {
                let decData = this.getDecompositionData(
                    decomp_type_id,
                    timescale_id,
                    start,
                    end
                );
                subject.next(decData);
            }, 10);
        }
        return subject;
    }

    getData_ForecastTimelabels(): TimeSelectorDataInput {
        let output = {
            order: this.dataModel.getTimeScalesOrder(),
            timescales: {}
        };
        let l = (output['order'] && output['order'].length)
            ? output['order'].length : 0;
        for (let i = 0; i < l; i++) {
            let ts = output['order'][i];
            output['timescales'][ts] = this.dataModel.getTimeLine(ts);
        }
        return output;
    }

    getDecompPeriodLabels(): TimeSelectorDataInput {
        let allowedTs = this.ddConfig['decomp_timescales'];
        let allTs = this.dataModel.getTimeScalesOrder();
        let order = [];
        for (let i = 0; i < allTs.length; i++) {
            if (allowedTs.indexOf(allTs[i]) != -1) {
                order.push(allTs[i]);
            }
        }
        let output = {
            order: order,
            timescales: {}
        };
        let l = (output['order'] && output['order'].length)
            ? output['order'].length : 0;
        for (let i = 0; i < l; i++) {
            let ts = output['order'][i];
            output['timescales'][ts] = this.dataModel.getTimeLine(ts);
        }
        return output;
    }

    getData_DriverSummaryTableData(start: string,
                                   end: string,
                                   mid: string,
                                   timescale: string,
                                   selRowId: string = null): ClickableTable {
        let drvSumTableIds = {};

        let variables = this.dataModel.getVariablesByType('driver');
        let timelabels = this.dataModel.getTimeLine(timescale, start, end);

        let vars: Array<TableWidgetRowColItem> = [],
            tls: Array<TableWidgetRowColItem> = [],
            vals: TableWidgetValues = {},
            timelines: Object = {},
            l: number;

        let growthLag = this.dataModel.getTimeScaleLag(timescale);

        // For ROWS
        l = (timelabels && timelabels.length) ? timelabels.length : 0;
        for (let i = 0; i < l; i++) {
            let timelabel = timelabels[i];
            let pTimelabel = this.dataModel.getParentTimelabel(timelabel.id,
                timelabel.timescale);

            let startTL = this.dataModel.getPreviousTimeLabel(timescale,
                timelabel.full_name, growthLag);

            let start: string = null,
                notSelectable: boolean = true;
            if (startTL) {
                start = startTL.full_name;
                notSelectable = false;
            }
            drvSumTableIds[timelabel.full_name] = {
                start: start,
                end: timelabel.full_name
            };
            tls.push({
                id: timelabel.id,
                parent_id: (pTimelabel) ? pTimelabel.id : null,
                meta: [
                    {name: timelabel.full_name}
                ],
                notSelectable: notSelectable
            });
            vals[timelabel.full_name] = {};
            if (!(timelabel.timescale in timelines)) {
                timelines[timelabel.timescale] = [];
            }
            timelines[timelabel.timescale].push(timelabel.full_name);
        }

        // For COLS
        l = (variables && variables.length) ? variables.length : 0;
        for (let i = 0; i < l; i++) {
            let variable = variables[i];
            vars.push({
                id: variable.id,
                parent_id: null,
                meta: [
                    {name: variable.full_name},
                    {name: variable.metric}
                ]
            });

            for (let timescaleId in timelines) {
                let timeline = timelines[timescaleId];
                let values = this.dataModel.getPointsValue(timescaleId,
                    variable.id, timeline);
                for (let j = 0; j < timeline.length; j++) {
                    vals[timeline[j]][variable.id] = values[j];
                }
                // if (values && values.length) {
                //     for (let j = 0; j < values.length; j++) {
                //         vals[values[j].timestamp][variable.id] = values[j].value;
                //     }
                // }
            }
        }

        // Add CAGRs
        let ids = ['cagr/' + start + '/' + mid, 'cagr/' + mid + '/' + end];
        drvSumTableIds[ids[0]] = {
            start: start,
            end: mid,
        };
        drvSumTableIds[ids[1]] = {
            start: mid,
            end: end,
        };
        tls.push({
            id: ids[0],
            parent_id: null,
            meta: [
                {name: this.config['cagr'] + ' ' + start + '/' + mid}
            ]
        });
        tls.push({
            id: ids[1],
            parent_id: null,
            meta: [
                {name: this.config['cagr'] + ' ' + mid + '/' + end}
            ]
        });
        vals[ids[0]] = {};
        vals[ids[1]] = {};

        l = (variables && variables.length) ? variables.length : 0;
        for (let i = 0; i < l; i++) {
            let variable = variables[i];

            vals[ids[0]][variable.id] = this.dataModel.getGrowthRate(
                variable.id, start, mid, timescale);
            vals[ids[1]][variable.id] = this.dataModel.getGrowthRate(
                variable.id, mid, end, timescale);
        }

        return {
            data: {
                selected_row_id: selRowId,
                appendix: [
                    <string>this.config['driver'],
                    <string>this.config['metric'],
                ],
                cols: vars,
                rows: tls,
                values: vals
            },
            rows_data: drvSumTableIds
        };
    }

    getFullPeriod(timescale: string, start: string,
                  end: string): Array<string> {
        let timelabels = this.dataModel.getTimeLine(timescale, start, end);
        return (timelabels && timelabels.length)
            ? timelabels.map((el) => {
            return el.full_name
        }) : [];
    }

    getFactorsList(decompType: string): Array<{id: string; name: string}> {
        let output = [];
        let factors = this.dataModel.getDecompTypeFactors(decompType);
        if (factors) {
            let l = factors.length;
            for (let i = 0; i < l; i++) {
                let variable = this.dataModel.getVariable(factors[i]);
                if (variable) {
                    output.push({
                        id: variable.id,
                        name: variable.full_name
                    });
                }
            }
        }
        return output;
    }


    /**
     * Returns data for Decomposition Types Switcher.
     * This data is ready to use in template
     * @param defaultVal
     * @returns {ButtonsGroupDataInput}
     */
    getDecompTypesSwitcherData(defaultVal: string): ButtonsGroupDataInput {

        let output = [];
        let autoSel = true,
            sel;
        let types = this.dataModel.getDecompositionTypes();

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


    getDriversForFactor(decompType: string, factorId: string): Array<string> {
        return this.dataModel.getFactorDrivers(factorId);
    }

    getLanguagePackForTimeSelector() {
        return {
            'apply': this.config['apply'],
            'cancel': this.config['cancel']
        }
    }
}
