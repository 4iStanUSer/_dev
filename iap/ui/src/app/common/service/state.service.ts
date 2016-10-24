import {Injectable} from '@angular/core';

export class PageState {

    constructor(
        public state: {[s: string]: any},
        public page: string,
        private service: StateService)
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
export class StateService {

    private stateStorage: {[s: string]: Object} = {};

    constructor() {
    }

    private init(): void {
        // TODO Implement init() method
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

    public getPageState(page: string): PageState {
        if (!this.stateStorage[page]) {
            try {
                this.stateStorage[page] = JSON.parse(localStorage.getItem(page));
            } catch (e) {
                this.stateStorage[page] = {};
            }
        }
        return new PageState(this.stateStorage[page], page, this);
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
