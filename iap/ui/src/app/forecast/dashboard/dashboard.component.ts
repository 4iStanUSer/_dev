import {Component, OnInit, ViewChild} from '@angular/core';
import {DataManagerService, Period} from './data-manager.service';
import {StaticDataService} from "../../common/service/static-data.service";
import {StateService, PageState} from "../../common/service/state.service";
import {WaterfallChartComponent} from "../../common/cmp/waterfall-chart/waterfall-chart.component";

@Component({
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    private pageName: string = 'dashboard';




    private currMode: string = 'summary';
    private currTimeScale: string = 'annual';
    private localConfig: Object = {
        'modes': [
            {
                'key': 'summary',
                'name': 'Summary'
            },
            {
                'key': 'detailed',
                'name': 'Detailed'
            },
            {
                'key': 'drivers',
                'name': 'Drivers'
            }
        ],
    };
    private period: Period = null;

    @ViewChild('decomposition') decompositionObj: WaterfallChartComponent;

    private state: PageState;
    private lang: Object;
    private config: Object;

    private outputVars: Array<string> = [];
    private driverVars: Array<string> = [];

    public summaryCagrsData: Array<Object> = null;
    public summaryOutputsShortData: Array<Object> = null;
    public summaryDecompData: Object = null;

    /*---valueOrGrowthSwitch---*/
    public absOrRate: string = 'rate';
    public absOrRateSwitchData: Array<Object> = [
        {
            key: 'absolute',
            name: 'Absolute values',
            selected: false
        },
        {
            key: 'rate',
            name: 'Growth rates',
            selected: true
        }
    ];
    public absOrRateSwitchConfig: Object = {};

    public absOrRateSwitchChanged(e) {
        console.log('absOrRateSwitchChanged');

        this.absOrRate = e['key'];
        this.state.set('abs_or_rate', this.absOrRate);

        if (this.decompositionObj) {
            this.decompositionObj.changeMode(this.absOrRate);
        }

        let outputVars = this.dm.getVarsByType('output');
        if (this.period) {
            if ('rate' == this.absOrRate && this.summaryCagrsData === null) {
                this.summaryCagrsData =
                    this.dm.getData_Donut(this.period, outputVars);
            } else if (this.summaryOutputsShortData === null) {
                this.summaryOutputsShortData =
                    this.dm.getData_Bar(this.period, outputVars, 'preview');
            }
        }
    }
    /*---.valueOrGrowthSwitch---*/
    /*---Decomposition---*/

    /*---.Decomposition---*/

    constructor(
        private dm: DataManagerService,
        private stateService: StateService, // TODO Review (VL)
        private sds: StaticDataService
    ) {
        this.state = this.stateService.getPageState(this.pageName);
        this.lang = this.sds.getLangPack(this.pageName);
        this.config = this.sds.getConfig(this.pageName);
    }

    ngOnInit() {
        let absOrRate = this.state.get('abs_or_rate');

        if (!absOrRate) {
            absOrRate = this.absOrRate;
            this.state.set('abs_or_rate', absOrRate);
        } else {
            this.absOrRate = absOrRate;
        }
        this.absOrRateSwitchData.forEach(function(el){
            if (this.absOrRate == el['key']) {
                el['selected'] = true;
            } else {
                el['selected'] = false;
            }
        }, this);

        this.dm.init().subscribe((d) => {
            this.period = this.dm.getInitialPeriod(this.currTimeScale);

            let outputVars = this.dm.getVarsByType('output');
            if (this.period) {
                if ('rate' == this.absOrRate) {
                    this.summaryCagrsData =
                        this.dm.getData_Donut(this.period, outputVars);
                } else {
                    this.summaryOutputsShortData =
                        this.dm.getData_Bar(this.period, outputVars, 'preview');
                }

                this.summaryDecompData =
                    this.dm.getData_Decomposition(this.period);
            }
        });


        //////////////////////////////////////////////////////////////////////
        // this.vTableData = this.dm.getData_VTable();
    }

    public changeMode(mode: string) {
        if (mode
            && this.localConfig['modes'].filter(function(el){
                return (el['key'] == mode) ? true : false;
            }, this) != -1)
        {
            this.currMode = mode;
        }
    }




    /**********TEMP***********/
    public showTable: boolean = false;
    public decompositionTableData: Object = {};
    public showDecompositionFull(data: Object) {
        this.decompositionTableData = this.dm.getData_VTable();
        this.showTable = !this.showTable;
    }
    ///////////
    public showFullCharts: boolean = false;
    public summaryOutputsFullData: Object = {};
    public showBarChartFull(data: Object) {
        let outputVars = this.dm.getVarsByType('output');

        if (data['name'] && outputVars.indexOf(data['name']) != -1) {
            this.summaryOutputsFullData = this.dm.getData_Bar(this.period, [data['name']], 'full');
        } else {
            this.summaryOutputsFullData = this.dm.getData_Bar(this.period, outputVars, 'full');
        }
        this.showFullCharts = !this.showFullCharts;
    }
    /**********.TEMP***********/


    private onTimePeriodChanged(newPeriod) {
        console.log(newPeriod);
    }
}
