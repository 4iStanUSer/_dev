import {Injectable} from '@angular/core';

@Injectable()
export class LanguageService {

    private data: {[s: string]: string} = {};

    constructor() {
    }

    public init(){
        // TODO Implement init() method
    }

    public getLangeagePack() {
        return this.data; // TODO Check this - maybe deepCopy is necessary
    }
}
