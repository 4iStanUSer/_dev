import {Injectable} from '@angular/core';

@Injectable()
export class StaticDataService {

    private _config: {[s: string]: Object} = null;

    private _lang: {[s: string]: Object} = null;

    constructor() {
        this.init();
    }

    private init(): void {
        // TODO Implement init() method
        this._config = {
            'dashboard': {
                'main_color': 'blue'
            }
        };
        this._lang = {
            'dashboard': {
                'decomposition': 'Decomposition'
            }
        };
    }
    private loadPageData(page: string): void {

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

}
