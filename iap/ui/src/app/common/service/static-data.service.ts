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

    private config: {[s: string]: Object} = {};

    private states: {[s: string]: PageState} = {};

    constructor() {
        // this.init();
    }

    private init(): void {
    }

    hasPage(page: string): boolean {
        return (this.pages.indexOf(page) != -1);
    }

    addPage(page: string, frontData: Object, data: Object = null) {
        if (this.pages.indexOf(page) == -1) {
            this.pages.push(page);

            let state = frontData['state'];
            if (data && data['state']) {
                for (let opt in state) {
                    if (typeof data['state'][opt] !== "undefined"
                        && data['state'][opt] !== null) {
                        state[opt] = data['state'][opt];
                    }
                }
            }
            this.states[page] = new PageState(state, page, this);

            this.config[page] = frontData['config'];
            if (data && data['config']) {
                for (let opt in this.config[page]) {
                    if (typeof data['config'][opt] !== "undefined"
                        && data['config'][opt] !== null) {
                        this.config[page][opt] = data['config'][opt];
                    }
                }
            }
        }
    }

    public getState(page: string): PageState {
        try {
            return this.states[page];
        } catch(e) {
            console.error('StaticDataService:', e);
        }
        return null;
    }

    public getConfig(page: string): Object {
        try {
            return this.config[page];
        } catch(e) {
            console.error('StaticDataService:', e);
        }
        return null;
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
        this.saveOutside(page, key, value); // TODO Review
    }

    public setPageState(pageState: PageState) {
        let page = pageState.page;
        for (let key in pageState.state) {
            this.saveOutside(page, key, pageState.state[key]);
        }
    }
}
