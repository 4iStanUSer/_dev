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

    public scenarios = [{"criteria": "USA-iPhone-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Draft", "id": 10, "name": "Price Growth Dynamics JJLean", "shared": "No", "scenario_permission": ["copy"], "description": "Dynamics of Price Growth in USA", "author": "user@mail.com"}, {"criteria": "USA-iPhone-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Draft", "id": 9, "name": "Price Growth Dynamics JJLean", "shared": "No", "scenario_permission": ["copy"], "description": "Dynamics of Price Growth in USA", "author": "user@mail.com"}, {"criteria": "USA-iPhone-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Draft", "id": 8, "name": "Price Growth Dynamics JJLean", "shared": "No", "scenario_permission": ["copy"], "description": "Dynamics of Price Growth in USA", "author": "user@mail.com"}, {"criteria": "USA-iPhone-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Draft", "id": 6, "name": "Price Growth Dynamics JJLean", "shared": "No", "scenario_permission": ["copy"], "description": "Dynamics of Price Growth in USA", "author": "user@mail.com"}, {"criteria": "Brazil-Nike-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Final", "id": 4, "name": "Price Growth Dynamics JJOralCare", "shared": "Yes", "scenario_permission": ["share", "change_status", "copy", "delete", "edit"], "description": "Dynamics of Price Growth in Brazil", "author": "default_user"}, {"criteria": "Brazil-Nike-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Final", "id": 3, "name": "Price Growth Dynamics JJOralCare", "shared": "Yes", "scenario_permission": ["share", "change_status", "copy", "delete", "edit"], "description": "Dynamics of Price Growth in Brazil", "author": "default_user"}, {"criteria": "Brazil-Nike-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Final", "id": 2, "name": "Price Growth Dynamics JJOralCare", "shared": "Yes", "scenario_permission": ["share", "change_status", "copy", "delete", "edit"], "description": "Dynamics of Price Growth in Brazil", "author": "default_user"}, {"criteria": "Brazil-Nike-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Final", "id": 5, "name": "Price Growth Dynamics JJOralCare", "shared": "Yes", "scenario_permission": ["share", "change_status", "copy", "delete", "edit"], "description": "Dynamics of Price Growth in Brazil", "author": "default_user"}, {"criteria": "Brazil-Nike-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Final", "id": 1, "name": "Price Growth Dynamics JJOralCare", "shared": "Yes", "scenario_permission": ["share", "change_status", "copy", "delete", "edit"], "description": "Dynamics of Price Growth in Brazil", "author": "default_user"}, {"criteria": "USA-iPhone-Main", "modify_date": "2017-04-13 10:30:12.605626", "favorite": "No", "status": "Draft", "id": 7, "name": "Price Growth Dynamics JJLean", "shared": "No", "scenario_permission": ["copy"], "description": "Dynamics of Price Growth in USA", "author": "user@mail.com"}]

    getScenariosListData(): Object[] {
        let scenarios_list = [];

        for (let i = 0; i < this.scenarios.length; i++) {
            let scenario_item = {
                'id': this.scenarios[i]['id'],
                'name': this.scenarios[i]['name'],
            };
            scenarios_list.push(scenario_item);
        }
        return scenarios_list;
    }

    getSimulatorData(): Promise<Object> {
      return Promise.resolve(this.simulator_data);
    }
}
