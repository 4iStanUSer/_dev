import {Injectable} from '@angular/core';

@Injectable()
export class StaticDataService {

    private _default: {[s: string]: Object} = null;

    private _config: {[s: string]: Object} = null;

    private _lang: {[s: string]: Object} = null;

    constructor() {
        this.init();
    }

    private init(): void {
        // TODO Implement init() method
        this._default = {
            'dashboard': {
                'forecast_timescale': 'annual', // annual|quarterly|monthly
                'forecast_absolute_rate': 'absolute', // absolute|rate
                'forecast_collapse_expand': 'collapse', // collapse|expand
                'forecast_active_tab': 'all', // all|(name of variable)
                'forecast_tab': 'all', // all|(or name of variable)
                'decomp_value_volume_price': 'Value', // value|volume|price (name of type)

                'd_summary_table_collapsed_expanded': 'expanded', // collapsed|expanded

                'd_details_table_collapsed_expanded': 'expanded', // collapsed|expanded

                'd_details_selected_megadriver': null, // null(get first)|mega driver key
            }
        };


        this._lang = {
            'dashboard': {
                'forecast_block': 'Forecast',
                'decomposition_block': 'Decomposition',
                'insights_block': 'Insights',
                'drivers_summary_block': 'Drivers Summary',

                'dashboard_tab': 'Dashboard',
                'drivers_summary_tab': 'Drivers Summary',
                'drivers_details_tab': 'Driver\'s Details',

                'value': 'Value',
                'growth_rate': 'Growth rate',
                'collapse': 'Collapse',
                'expand': 'Expand',
                'explore': 'Explore',
                'tab_all': 'All',
                'absolute': 'Absolute',
                'growth_cagr': 'Growth (CAGR)',

                'driver_contribution': 'Driver Contribution to Sales Growth,',
                'driver_change_cagr': 'Driver Change (CAGR)',

                'driver': 'Driver',
                'metric': 'Metric',
                'cagr': 'CAGR',

                'sub_drivers_dynamic': 'Sub-driver\'s dynamic',
                'sub_drivers_impact': 'Sub-driver\'s impact',
                'fact': 'Fact',
            }
        };

        this._config = { // ...
            'dashboard': {
                'decomp_timescales': ['annual'],

                ////////////
                'main_color': 'blue'
            }
        };
    }
    private loadPageData(page: string): void {

    }



    public getDefaults(page: string): Object {
        // TODO Implement getDefaults() method
        if (!page) {
            console.error('StaticDataService empty query');
            return false;
        }
        if (!(page in this._default)) {
            // TODO Implement procedure for getting more pages' packages
        } else {
            return this._default[page]; // TODO Check this - maybe deepCopy is necessary
        }
    }
    public getLangPack(page: string): Object {
        // TODO Implement getLangPack() method
        if (!page) {
            console.error('StaticDataService empty query');
            return false;
        }
        if (!(page in this._lang)) {
            // TODO Implement procedure for getting more pages' packages
        } else {
            return this._lang[page]; // TODO Check this - maybe deepCopy is necessary
        }
    }

    public getConfig(page: string): Object {
        if (!page) {
            console.error('StaticDataService empty query');
            return false;
        }
        if (!(page in this._config)) {
            // TODO Implement procedure for getting more configs
        } else {
            return this._config[page]; // TODO Check this - maybe deepCopy is necessary
        }
    }

}
