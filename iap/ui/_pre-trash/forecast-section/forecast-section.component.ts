import {
    Component,
    OnInit,
    OnChanges,
    Input,
    SimpleChanges
} from '@angular/core';
import {
    // PointsValuesModel,
    PointValueModel
} from "./../../../common/model/points-values.model";
// import {CagrsModel} from "./../../../common/model/cagrs.model";
// import {
//     TimeLabelsModel,
//     TimeLabelModel
// } from "./../../../common/model/time-labels.model";
import {DataModel} from "./../../../common/model/data.model";
import {VariableModel} from "../../../common/model/variables.model";

interface ChartInput {
    variable: Object;
    cagrs: any;
    data: any;
}
interface PeriodsInput {

}

@Component({
    selector: 'forecast-section',
    templateUrl: 'forecast-section.component.html',
    styleUrls: ['forecast-section.component.css']
})
export class ForecastSectionComponent implements OnInit, OnChanges {

    @Input('data-model') dataModel: DataModel = null;
    @Input('data-config') dataConfig: {
        timescale: string,
        varsToShow: Array<string>,
        periods: {
            short: Array<string>,
            full: Array<string>
        }
    } = null;
    @Input('config') config: Object = null;

    private totalTab: {
        short_data: Array<Object>, //Array<PointValueModel>,
        full_data: Array<Object>, //Array<PointValueModel>,
    } = null;
    private tabs: Array<{
        variable: VariableModel,
        short_data: Array<Object>, //Array<PointValueModel>,
        full_data: Array<Object>, //Array<PointValueModel>,
    }> = [];

    private lang: Object = {
        'active_all_tab': 'All',
        'passive_all_tab': 'Show All',
        'absolute': 'Absolute',
        'growth_cagr': 'Growth (CAGR)',
        'expand': 'Expand',
        'collapse': 'Collapse'
    };

    private conf: Object = {
        default_state: {
            view_mode: 'short', // 'full',
            tab: 'all' // or name of variable
        },
        colors: {
            hue: {
                cagr_plus: 130,
                cagr_minus: 30
            },
            lightnesse: {
                text: 50,
                background: 70
            },
            saturation: 100
        }
    };

    private state: Object = {
        currTabIndex: -1, // indexes of this.tabs
        currViewMode: 'short' // || 'full'
    };

    ngOnChanges(ch: SimpleChanges) {
        if (ch['dataModel']) {
            this.dataModel = ch['dataModel']['currentValue'];
        }
        if (ch['dataConfig']) {
            this.dataConfig = ch['dataConfig']['currentValue'];
        }
        if (ch['config']) {

        }

        this.tabs = [];
        let timescale = this.dataConfig['timescale'];

        this.totalTab = {
            short_data: [],
            full_data: []
        };
        for (let i = 0; i < this.dataConfig['varsToShow'].length; i++) {
            let variable = this.dataModel.getVariable(
                this.dataConfig['varsToShow'][i]
            );
            let list: Array<PointValueModel>;

            // Short data
            list = this.dataModel.getPointsValue(
                timescale,
                this.dataConfig['varsToShow'][i],
                this.dataConfig['periods']['short']
            );
            let short_data = this.convertForBarChart(variable, list,
                this.getCagrPeriods(list));

            // Full data
            list = this.dataModel.getPointsValue(
                timescale,
                this.dataConfig['varsToShow'][i],
                this.dataConfig['periods']['full']
            );
            let periodsForFull = this.getCagrPeriods(list);
            // TODO Add periods for middle point
            let full_data = this.convertForBarChart(variable, list,
                periodsForFull);

            this.tabs.push({
                variable: variable,
                short_data: [short_data],
                full_data: [full_data]
            });
            this.totalTab['short_data'].push(short_data);
            this.totalTab['full_data'].push(full_data);
        }
    }

    private convertForBarChart(
        variable: VariableModel,
        pointsValues: Array<PointValueModel>,
        cagrPeriods: Array<{start: string, end: string}>
    ) { // TODO Move to upper (common) level (VL)

        let cagrs = this.dataModel.getCargsForPointsValues(variable,
            cagrPeriods);

        return {
            'name': variable.name + ', ' + variable.metric,
            'variable': variable,
            'cagrs': cagrs, // TODO Check!!! when cagrs will be available
            'data': pointsValues.map((el)=> {
                return {
                    'name': el['timestamp'],
                    'value': el['value'] // TODO Add ability to chose between abs values & growth rate (VL)
                };
            })
        };
    }

    private getCagrPeriods(points: Array<PointValueModel>) : Array<{
        'start': string,
        'end': string
    }> { // TODO Move to upper (common) level (VL)
        let timestamps = points.map((p) => {
            return p.timestamp;
        });

        let periods = [];
        for (let i = 0; i < timestamps.length - 1; i++) {
            periods.push({
                'start': timestamps[i],
                'end': timestamps[i + 1],
            });
        }
        return periods;
    }

    constructor() {
    }

    ngOnInit() {
    }

    private onTabClick(index: number) {
        if (
            (index > -1 && index < this.tabs.length)
            ||
            (index == -1)
        ) {
            this.state['currTabIndex'] = index;
        } else {
            console.error('No such tab!');
        }
    }

    private onExpandCollapseButtonClick() {
        let mode = (this.state['currViewMode'] == 'full') ? 'short' : 'full';
        this.changeViewMode(mode);
    }

    private changeViewMode(mode: string) {
        this.state['currViewMode'] = mode;
    }

}
