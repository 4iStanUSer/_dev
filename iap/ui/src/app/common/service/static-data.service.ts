import {Injectable} from '@angular/core';


export class PageState {

    constructor(
        public state: {[s: string]: any},
        public page: string,
        private service: StaticDataService)
    {
        if (!this.state) this.state = {};
    }

    public get(key: string) {
        return this.state[key];
    }

    public set(key: string, value: any) {
        this.state[key] = value;
        this.service.setPageStateKey(this.page, key, value);
    }

    public save() {
        this.service.setPageState(this);
    }

}

@Injectable()
export class StaticDataService {
    private pages: Array<string> = [];

    private defState: {[s: string]: Object} = null; // TODO Solve to remove

    private config: {[s: string]: Object} = null;

    // private _lang: {[s: string]: Object} = null;

    constructor() {
        // this.init();
    }

    private init(): void {
        // TODO Implement init() method
        // this._default = {
        //     'dashboard': {
        //         'forecast_timescale': 'annual', // annual|quarterly|monthly
        //         'forecast_absolute_rate': 'absolute', // absolute|rate
        //         'forecast_collapse_expand': 'collapse', // collapse|expand
        //         'forecast_active_tab': 'all', // all|(name of variable)
        //         'forecast_tab': 'all', // all|(or name of variable)
        //         'decomp_value_volume_price': 'Value', // value|volume|price (name of type)
        //
        //         'd_summary_table_collapsed_expanded': 'expanded', // collapsed|expanded
        //
        //         'd_details_table_collapsed_expanded': 'expanded', // collapsed|expanded
        //
        //         'd_details_selected_megadriver': null, // null(get first)|mega driver key
        //     }
        // };
        //
        //
        // this._lang = {
        //     'dashboard': {
        //         'forecast_block': 'Forecast',
        //         'decomposition_block': 'Decomposition',
        //         'insights_block': 'Insights',
        //         'drivers_summary_block': 'Drivers Summary',
        //
        //         'dashboard_tab': 'Dashboard',
        //         'drivers_summary_tab': 'Drivers Summary',
        //         'drivers_details_tab': 'Driver\'s Details',
        //
        //         'value': 'Value',
        //         'growth_rate': 'Growth rate',
        //         'collapse': 'Collapse',
        //         'expand': 'Expand',
        //         'explore': 'Explore',
        //         'tab_all': 'All',
        //         'absolute': 'Absolute',
        //         'growth_cagr': 'Growth (CAGR)',
        //
        //         'driver_contribution': 'Driver Contribution to Sales Growth,',
        //         'driver_change_cagr': 'Driver Change (CAGR)',
        //
        //         'driver': 'Driver',
        //         'metric': 'Metric',
        //         'cagr': 'CAGR',
        //
        //         'sub_drivers_dynamic': 'Sub-driver\'s dynamic',
        //         'sub_drivers_impact': 'Sub-driver\'s impact',
        //         'fact': 'Fact',
        //     }
        // };
        //
        // this._config = { // ...
        //     'dashboard': {
        //         'decomp_timescales': ['annual'],
        //
        //         ////////////
        //         'main_color': 'blue'
        //     }
        // };
    }

    hasPage(page: string): boolean {
        return (this.pages.indexOf(page) != -1);
    }

    addPage(page: string, data: Object) {
        if (this.pages.indexOf(page) == -1) {
            this.pages.push(page);
            if (!this.defState) {
                this.defState = {};
            }
            this.defState[page] = data['state'];


            // Merge defaults into state
            let defKeys = Object.keys(this.defState[page]),
                defKeysLen = defKeys.length,
                defKey = null;
            for (let i = 0; i < defKeysLen; i++) {
                defKey = defKeys[i];
                let v = this.state.get(defKey);
                if (v === null || v === undefined) {
                    this.state.set(defKey, this.defaults[defKey]);
                }
            }





            if (!this.config) {
                this.config = {};
            }
            this.config[page] = data['config'];
            // this._lang[page] = data['lang'];
        }
    }

    private loadPageData(page: string): void {

    }


    public getState(page: string): PageState {
        return this.getPageState(page); // TODO Implement
    }
    public getConfig(page: string): Object {
        if (!page) {
            console.error('StaticDataService empty query');
            return false;
        }
        if (!(page in this.config)) {
            // TODO Implement procedure for getting more configs
        } else {
            return this.config[page]; // TODO Check this - maybe deepCopy is necessary
        }
    }

    // public getLangPack(page: string): Object {
    //     // TODO Implement getLangPack() method
    //     if (!page) {
    //         console.error('StaticDataService empty query');
    //         return false;
    //     }
    //     if (!(page in this._lang)) {
    //         // TODO Implement procedure for getting more pages' packages
    //     } else {
    //         return this._lang[page]; // TODO Check this - maybe deepCopy is necessary
    //     }
    // }


    // - FROM STATE SERVICE
    private stateStorage: {[s: string]: Object} = {}; // TODO TEMP !!!
    private storage: {[s: string]: PageState} = {};

    public getPageState(page: string) { //: Observable<PageState>
        if (!this.storage[page]) {
            if (!this.stateStorage[page]) {
                try {
                    this.stateStorage[page] =
                        JSON.parse(localStorage.getItem(page));
                } catch (e) {
                    this.stateStorage[page] = {};
                }
            }
            this.storage[page] = new PageState(this.stateStorage[page],
                page, this)
        }
        return this.storage[page];
        // TODO Make request to server (VL)
        // let resp = new Observable(observer => {
        //     setTimeout(() => {
        //         observer.next(this.storage[page]);
        //     },5000);
        // });
        // return resp;
    }

    private saveOutside(page: string, key: string, value: any) {
        let pageValue;
        try {
            pageValue = JSON.parse(localStorage.getItem(page));
        } catch (e) {
            pageValue = {};
        }
        if (!pageValue) pageValue = {};
        pageValue[key] = value;
        localStorage.setItem(page, JSON.stringify(pageValue));
    }



    public setPageStateKey(page: string, key: string, value: any) {
        try {
            this.stateStorage[page][key];
        } catch(e) {
            this.stateStorage[page] = {};
        }
        this.stateStorage[page][key] = value;
        this.saveOutside(page, key, value); // TODO Review
    }

    public setPageState(pageState: PageState) {
        let page = pageState.page;
        for (let key in pageState.state) {
            this.saveOutside(page, key, pageState.state[key]);
        }
    }
}
