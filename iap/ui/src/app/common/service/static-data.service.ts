import {Injectable} from '@angular/core';

/**
 * Storage for holding dynamic page state - selections, modes, etc.
 * Instances of this type create and save inside StaticDataService.
 * They should be used in pages components or their services.
 */
export class PageState {
    constructor(
        public state: {[s: string]: any},
        public page: string,
        private service: StaticDataService)
    {
        if (!this.state) this.state = {};
    }

    /**
     * Returns value with current state of requested key
     * @param key
     * @returns {any}
     */
    public get(key: string) {
        return this.state[key];
    }

    /**
     * Saves value as current state for passed key
     * @param key
     * @param value
     */
    public set(key: string, value: any) {
        this.state[key] = value;
        this.service.setPageStateKey(this.page, key, value);
    }

    /**
     * Saves itself by calling .setPageState() on StaticDataService
     */
    public save() {
        this.service.setPageState(this);
    }
}

@Injectable()
/**
 * Service for holding locally static data(labels, configurations) for pages.
 * Main aim - send only one request for getting static data for page
 * while frontend application is alive.
 */
export class StaticDataService {
    // TODO Make this service smarter - get page data inside this service

    /**
     * List of loaded pages
     * @type {Array}
     */
    private pages: Array<string> = [];

    /**
     * Storage of page static data. As key - page name.
     * @type {Object}
     */
    private config: {[s: string]: Object} = {};

    /**
     * Storage of PageState objects. As key - page name.
     * @type {Object}
     */
    private states: {[s: string]: PageState} = {};

    constructor() {
    }

    private init(): void {
    }

    /**
     * Checks if data for page was loaded
     * @param page
     * @returns {boolean}
     */
    hasPage(page: string): boolean {
        return (this.pages.indexOf(page) != -1);
    }

    /**
     * Adds page data into state storage and config storage.
     * Variable 'data' has higher priority than 'frontData'
     * that is why values from 'data' rewrite values from 'frontData'
     * @param page string - page name
     * @param frontData {state: Object, config: Object} - data defined in JS
     * @param data {state: Object, config: Object} - data received from server
     */
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

    /**
     * Returns PageState object from state storage for requested page.
     * If data wasn't found - return null.
     * @param page
     * @returns {PageState}
     */
    public getState(page: string): PageState {
        try {
            return this.states[page];
        } catch(e) {
            console.error('StaticDataService:', e);
        }
        return null;
    }

    /**
     * Returns Object with static data for requested page.
     * If data wasn't found - return null.
     * @param page
     * @returns {Object}
     */
    public getConfig(page: string): Object {
        try {
            return this.config[page];
        } catch(e) {
            console.error('StaticDataService:', e);
        }
        return null;
    }

    /**
     * Saves page state in browser localStorage.
     * It uses by PageState objects for saving state
     * @param page
     * @param key
     * @param value
     */
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

    /**
     * Saves one key for page state externally
     * @param page
     * @param key
     * @param value
     */
    setPageStateKey(page: string, key: string, value: any) {
        this.saveOutside(page, key, value); // TODO Review - maybe remove
    }

    /**
     * Saves entirely page state externally
     * @param pageState
     */
    setPageState(pageState: PageState) { // TODO Review - maybe remove
        let page = pageState.page;
        for (let key in pageState.state) {
            this.saveOutside(page, key, pageState.state[key]);
        }
    }
}
