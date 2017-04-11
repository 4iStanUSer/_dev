import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';



@Injectable()
export class SimulatorService {
    public simulator_data: Object = {
        'value_volume_price': 'value'
    };
    /*
    private getCustomDataUrl = '/forecast/get_custom_data';

    constructor(private __http: Http) { }

    getData(): Promise<Object> {
        return this.__http.get(this.getCustomDataUrl)
               .toPromise()
               .then(response => response.json().data as Object);
    }
    */

    getSimulatorData(): Promise<Object> {
      return Promise.resolve(this.simulator_data);
    }
}
