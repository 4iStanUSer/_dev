import {Injectable} from '@angular/core';

import {Subject} from 'rxjs/Subject';

/*======TEMP=====*/
import {
    selectorsDataTEMP, selectorsConfigTEMP,
    // vertTableTEMP,
    // forecastValueRateData
} from './general/data';
/*======.TEMP=====*/


import {AjaxService} from "./../../common/service/ajax.service";
import {DataModel} from "./../../common/model/data.model";
// import {
//     TimePeriodInput,
//     TimePeriodModel
// } from "../../common/model/time-period.model";
import {StateService, PageState} from "../../common/service/state.service";
import {StaticDataService} from "../../common/service/static-data.service";
import {PointValueModel} from "../../common/model/points-values.model";
import {InsightInput} from "./insights/insights.component";
import {
    TableWidgetData,
    TableWidgetRowColItem,
    TableWidgetValues
} from "../../common/cmp/table-widget/table-widget.component";
import {DecompositionModel} from "../../common/model/decomposition.model";
import {TimelabelInput} from "../../common/model/time-labels.model";
import {ButtonsGroupDataInput} from "../../common/cmp/buttons-group/buttons-group.component";
import {
    VariableData, ClickableTable,
    DecompositionTypeData
} from "./interfaces";
import {TimeSelectorDataInput} from "../../common/cmp/time-selector/time-selector.component";


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

    dataModel: DataModel = null;

    decompModel: DecompositionModel = null;

    insights: Array<InsightInput> = [];

    lang: Object = null;

    state: PageState = null;

    config: Object = null; // TODO Interface for config

    initResolver: Subject<number> = null;

    periods: {
        main: Period,
        decomp: Period
    } = {
        main: null,
        decomp: null
    };
    // ----------------------------- //

    selectors: {data: Object, config: Object} = null;
    inputData: Object = null;// TODO Solve about this variable


    private defaults: Object = null; // TODO Review this variable (VL)

    constructor(private req: AjaxService,
                private stateService: StateService,
                private sds: StaticDataService) {

        this.init();
    }

    init() {
        if (!this.initResolver) {
            this.initResolver = new Subject();
            this.initDynamicData();
            this.initStaticData();
            this.initResolver.subscribe(() => {
                console.log('DataManager init() subscriber');
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

    private initDynamicData(): void {
        if (this.isData['dynamic']['sent']) return;

        this.isData['dynamic']['sent'] = true;
        this.isData['dynamic']['received'] = false;

        this.req.get({
            'url': '/forecast/get_dashboard_data',
            'data': {
                'entities_ids': [2]
            }
        }).subscribe((data)=> {
            this.isData['dynamic']['received'] = true;

            let d = data['data'];
            let c = data['config'];

            this.config = c;

            this.insights = d['insights'];

            this.periods['main'] = new Period(
                c['main_period']['timsecale'], // TODO Fix key
                c['main_period']['start'],
                c['main_period']['end'],
                '2015' //c['main_period']['mid'] // TODO Replace
            );
            this.periods['decomp'] = new Period(
                c['decomp_period']['timescale'],
                '2015', //c['decomp_period']['start'], // TODO Replace
                c['decomp_period']['end']
            );

            ////////////////////
            this.selectors = {
                data: selectorsDataTEMP,
                config: selectorsConfigTEMP
            };

            this.inputData = d; // TODO Remove this variable

            this.dataModel = new DataModel(
                d['timescales'],
                d['timelabels'],
                d['variables'],
                d['growth'],
                d['data']
            );
            let decompTypes = (c['factors_drivers'])
                ? Object.keys(c['factors_drivers']) : [];

            this.decompModel = new DecompositionModel(decompTypes,
                d['decomposition']);

            // console.log(this.dataModel);
            // console.log(this.decompModel);

            ////////////////////

            this.isData['dynamic']['processed'] = true;

            this.resolveInitObervable();
        });
    }

    private initStaticData() {
        if (this.isData['static']['sent']) return;

        this.isData['static']['sent'] = true;
        this.isData['static']['received'] = false;

        this.req.get({
            'url': '/forecast/get_page_configuration',
            'data': {
                'page_name': this.pageName
            }
        }).subscribe((d)=> {
            // this.isData['static']['received'] = true;
            //
            // this.lang = this.sds.getLangPack(this.pageName);
            // this.config = this.sds.getConfig(this.pageName);
            //
            // this.state = this.stateService.getPageState(this.pageName);
            // this.defaults = this.sds.getDefaults(this.pageName);
            //
            // // Merge defaults into state
            // let defKeys = Object.keys(this.defaults),
            //     defKeysLen = defKeys.length,
            //     defKey = null;
            // for (let i = 0; i < defKeysLen; i++) {
            //     defKey = defKeys[i];
            //     let v = this.state.get(defKey);
            //     if (v === null || v === undefined) {
            //         this.state.set(defKey, this.defaults[defKey]);
            //     }
            // }
            //
            // this.resolveInitObervable();
        });
        /////////////////////////////////////////
        this.isData['static']['received'] = true;

        this.lang = this.sds.getLangPack(this.pageName);
        this.config = this.sds.getConfig(this.pageName);

        this.state = this.stateService.getPageState(this.pageName);
        this.defaults = this.sds.getDefaults(this.pageName);

        // Merge defaults into state
        let defKeys = Object.keys(this.defaults),
            defKeysLen = defKeys.length,
            defKey = null;
        for (let i = 0; i < defKeysLen; i++) {
            defKey = defKeys[i];
            let v = this.state.get(defKey);
            if (v === null || v === undefined) {
                this.state.set(defKey, this.defaults[defKey]);
            }
        }
        this.resolveInitObervable();
        /////////////////////////////////////////
    }


    getState() {
        // this.stateService.getPageState(this.pageName)
        //     .subscribe((pageState) => {
        //
        //         console.log('getState subs');
        //
        //         this.state = pageState;
        //         this.checkFilling();
        //     });

        this.state = this.stateService.getPageState(this.pageName);
        this.defaults = this.sds.getDefaults(this.pageName);

        // Merge defaults into state
        let defKeys = Object.keys(this.defaults),
            defKeysLen = defKeys.length,
            defKey = null;
        for (let i = 0; i < defKeysLen; i++) {
            defKey = defKeys[i];
            let v = this.state.get(defKey);
            if (v === null || v === undefined) {
                this.state.set(defKey, this.defaults[defKey]);
            }
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
     * @param timescale
     * @param timepoints
     * @param variable
     * @param cagrsPeriod
     * @returns {VariableData}
     */
    getVariableData(timescale: string,
                    timepoints: Array<string>,
                    variable: string,
                    cagrsPeriod: Period = null): VariableData {

        let pointsValue: Array<PointValueModel>;
        let output: VariableData = {
            abs: [],
            rate: [],
            cagr: null
        };

        pointsValue = this.dataModel.getPointsValue(timescale, variable,
            timepoints);
        for (let j = 0; j < pointsValue.length; j++) {
            output.abs.push({
                name: pointsValue[j].timestamp, // OR timelabel.full_name
                value: pointsValue[j].value
            });
        }
        for (let i = 0; i < timepoints.length - 1; i++) {
            let start = timepoints[i];
            let end = timepoints[i + 1];
            let growth = this.dataModel.getGrowthRate(variable, start,
                end, timescale);
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
                        variable,
                        cagrsPeriod.start,
                        cagrsPeriod.mid,
                        cagrsPeriod.timescale)
                },
                {
                    start: cagrsPeriod.mid,
                    end: cagrsPeriod.end,
                    value: this.dataModel.getGrowthRate(
                        variable,
                        cagrsPeriod.mid,
                        cagrsPeriod.end,
                        cagrsPeriod.timescale)
                },
            ]
        }
        return output;
    }

    /**
     * Returns Decomposition's Data:
     * absolute values, rates and and item changes
     * @param type
     * @param timescale
     * @param start
     * @param end
     * @returns {DecompositionTypeData}
     */
    getDecompositionData(type: string, timescale: string,
                         start: string, end: string): DecompositionTypeData {
        let output = {
            'abs': [],
            'rate': [],
            'table': []
        };
        let items = this.decompModel.getDecomposition(type, start, end);
        let l = (items && items.length) ? items.length : 0;
        for (let i = 0; i < l; i++) {
            output['abs'].push({
                name: items[i]['name'],
                value: items[i]['value'],
                metric: '',
            });
            output['rate'].push({
                name: items[i]['name'],
                value: items[i]['growth'],
                metric: '%',
            });
            if (i != 0 && i != l - 1) {
                output['table'].push({
                    name: items[i]['name'],
                    value: items[i]['growth'],
                    metric: '%',
                });
            }
        }
        return output;
    }

    // getData_ForecastRateValues(timescale: string, timepoints: Array<string>,
    //                            variable: string) {
    //     return null; // TODO Implement
    // }

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
        let allowedTs = this.config['dec_timescales'];
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
                id: timelabel.full_name,
                parent_id: (timelabel.parent)
                    ? timelabel.parent.full_name : null,
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
                id: variable.key,
                parent_id: null,
                meta: [
                    {name: variable.name},
                    {name: variable.metric}
                ]
            });

            for (let timescaleKey in timelines) {
                let timeline = timelines[timescaleKey];
                let values = this.dataModel.getPointsValue(timescaleKey,
                    variable.key, timeline);
                if (values && values.length) {
                    for (let j = 0; j < values.length; j++) {
                        vals[values[j].timestamp][variable.key] = values[j].value;
                    }
                }
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
                {name: this.lang['cagr'] + ' ' + start + '/' + mid}
            ]
        });
        tls.push({
            id: ids[1],
            parent_id: null,
            meta: [
                {name: this.lang['cagr'] + ' ' + mid + '/' + end}
            ]
        });
        vals[ids[0]] = {};
        vals[ids[1]] = {};

        l = (variables && variables.length) ? variables.length : 0;
        for (let i = 0; i < l; i++) {
            let variable = variables[i];

            vals[ids[0]][variable.key] = this.dataModel.getGrowthRate(
                variable.key, start, mid, timescale);
            vals[ids[1]][variable.key] = this.dataModel.getGrowthRate(
                variable.key, mid, end, timescale);
        }

        return {
            data: {
                selected_row_id: selRowId,
                appendix: [
                    <string>this.lang['driver'],
                    <string>this.lang['metric'],
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

    getMegaDriversList(decompType: string): Array<{id: string; name: string}> {
        let megaDrvsKeys: Array<string>;
        try {
            megaDrvsKeys = Object.keys(
                this.config['factors_drivers'][decompType]);
        } catch (e) {
            console.error('Have no such decomposition type', decompType);
            return null;
        }
        let output: Array<{id: string; name: string}> = [];
        let l = megaDrvsKeys.length;
        if (l > 0) {
            for (let i = 0; i < l; i++) {
                let megaDrvsKey = megaDrvsKeys[i];
                // TODO Add name for mega drivers
                output.push({
                    id: megaDrvsKey,
                    name: megaDrvsKey
                });
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
        let types = this.decompModel.getDecompositionTypes();

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


    getDriversOfMegaDriver(decompType: string, megaDrv: string): Array<string> {
        // Get all drivers for megadriver and decomposition type
        let allDrv: Array<string>;
        try {
            allDrv = this.config['factors_drivers'][decompType][megaDrv];
        } catch (e) {
            console.error('Have no data', decompType, megaDrv, e);
        }
        let output: Array<string> = [];

        // // Filter only existing drivers
        // output = allDrv.filter((variable) => {
        //     return this.dataModel.variableExists(variable);
        // }, this);
        output = allDrv;
        return output;
    }
}
