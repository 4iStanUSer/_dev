import {Injectable} from '@angular/core';

@Injectable()
export class ConfigurationService {

    private data: {[s: string]: Object} = {};

    constructor() {
    }

    public init(){
        // TODO Implement init() method
        this.data = {
            'dashboard': {


            }
        };
    }

    public getConfig(page: string) {
        if (!page) {
            console.error('ConfigurationService empty query');
            return false;
        }
        if (!(page in this.data)) {
            // TODO Implement procedure for getting more configs
        } else {
            return this.data[page]; // TODO Check this - maybe deepCopy is necessary
        }
    }

}
