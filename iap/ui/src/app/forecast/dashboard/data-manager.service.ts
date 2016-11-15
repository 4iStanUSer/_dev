import {Injectable} from '@angular/core';

import {Subject} from 'rxjs/Subject';

/*======TEMP=====*/
import {
    selectorsDataTEMP, selectorsConfigTEMP, vertTableTEMP,
    forecastValueRateData
} from './general/data';
/*======.TEMP=====*/


import {AjaxService} from "./../../common/service/ajax.service";
import {DataModel} from "./../../common/model/data.model";
import {
    TimePeriodInput,
    TimePeriodModel
} from "../../common/model/time-period.model";
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


class Period {
    constructor(
        public timescale: string = null,
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
            this.decompModel = new DecompositionModel(d['decomposition']);

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

    getData_ForecastAbsValues(timescale: string, timepoints: Array<string>, variable: string) {
        let pointsValue: Array<PointValueModel>;
        let output: {
            absolute: Array<{name: string, value: number}>,
            rate: Array<number>
        } = {
            absolute: [],
            rate: []
        };

        pointsValue = this.dataModel.getPointsValue(timescale, variable,
            timepoints);
        for (let j = 0; j < pointsValue.length; j++) {
            output['absolute'].push({
                name: pointsValue[j].timestamp, // OR timelabel.full_name
                value: pointsValue[j].value
            });
        }
        for (let i = 0;i<timepoints.length-1;i++) {
            let start = timepoints[i];
            let end = timepoints[i+1];
            let growth = this.dataModel.getGrowthRate(variable, start,
                end, timescale);
            output['rate'].push(growth);
        }
        return output;
    }

    getData_ForecastRateValues(timescale: string, timepoints: Array<string>,
                               variable: string) {
        return null; // TODO Implement
    }

    getData_ForecastTimelabels() {
        return this.inputData['timelabels'];
    }


    getData_Decomposition(type: string, timescale: string,
                          start: string, end: string) {
        let output = {
            'abs': [],
            'rate': [],
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
        }
        return output;
    }

    getDecompPeriodLabels() {
        let timescales = this.config['dec_timescales']; //decomp_timescales
        let output: Array<TimelabelInput> = [];

        // TODO Remake PeriodSelector Input data

        for (let i = 0; i < this.inputData['timelabels'].length; i++) {
            let timelabel = this.inputData['timelabels'][i];
            if (timescales.indexOf(timelabel['timescale']) != -1) {
                output.push(timelabel);
            }
        }
        return output;
    }

    private drvSumTableIds: {
        [id: string]: {
            start: string,
            end: string
        }
    } = {};
    convertDrvSumTableIdsIntoPeriod(id: string) {
        return this.drvSumTableIds[id];
    }
    getData_DriverSummaryTableData(start: string,
                                   end: string,
                                   mid: string,
                                   timescale: string,
                                   selRowId: string = null): TableWidgetData {
        // TODO Implement period limitations
        this.drvSumTableIds = {};

        let variables = this.dataModel.getVariablesByType('driver');
        let timelabels = this.dataModel.getPlainTimeLabels();

        let vars: Array<TableWidgetRowColItem> = [],
            tls: Array<TableWidgetRowColItem> = [],
            vals: TableWidgetValues = {},
            timelines: Object = {},
            l: number;

        // For ROWS
        l = (timelabels && timelabels.length) ? timelabels.length : 0;
        for (let i = 0; i < l; i++) {
            let timelabel = timelabels[i];
            this.drvSumTableIds[timelabel.full_name] = {
                // TODO Get from CAGR data
                start: timelabel.full_name,
                end: (parseInt(timelabel.full_name)+1).toString(),
            };
            tls.push({
                id: timelabel.full_name,
                parent_id: (timelabel.parent)
                    ? timelabel.parent.full_name : null,
                meta:[
                    {name: timelabel.full_name}
                ]
            });
            vals[timelabel.full_name] = {};
            if (!(timelabel.timescale in timelines)) {
                timelines[timelabel.timescale] = [];
            }
            timelines[timelabel.timescale].push(timelabel.full_name);
        }
        tls[tls.length-1]['notSelectable'] = true;

        // For COLS
        l = (variables && variables.length) ? variables.length : 0;
        for (let i = 0; i < l; i++) {
            let variable = variables[i];
            vars.push({
                id: variable.key,
                parent_id: null,
                meta:[
                    {name: variable.name},
                    {name: variable.metric}
                ]
            });

            for (let timescaleKey in timelines) {
                let timeline = timelines[timescaleKey];
                let values = this.dataModel.getPointsValue(timescaleKey,
                    variable.key, timeline);
                if (values && values.length) {
                    for (let j=0;j<values.length;j++) {
                        vals[values[j].timestamp][variable.key] = values[j].value;
                    }
                }
            }
        }

        // Add CAGRs
        let ids = ['cagr/'+start+'/'+mid, 'cagr/'+mid+'/'+end];
        this.drvSumTableIds[ids[0]] = {
            // TODO Get from CAGR data
            start: start,
            end: mid,
        };
        this.drvSumTableIds[ids[1]] = {
            // TODO Get from CAGR data
            start: mid,
            end: end,
        };
        tls.push({
            id: ids[0],
            parent_id: null,
            meta:[
                {name: this.lang['cagr'] + ' ' + start + '/' + mid}
            ]
        });
        tls.push({
            id: ids[1],
            parent_id: null,
            meta:[
                {name: this.lang['cagr'] + ' ' +  mid + '/' + end}
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
            selected_row_id: selRowId,
            appendix: [
                <string>this.lang['driver'],
                <string>this.lang['metric'],
            ],
            cols: vars,
            rows: tls,
            values: vals
        };
    }

    getFullPeriod(timescale: string, start: string,
                  end: string): Array<string> {
        let timelabels = this.dataModel.getTimeLine(timescale, start, end);
        return (timelabels && timelabels.length)
            ? timelabels.map((el) => {return el.full_name}) : [];
    }

}
