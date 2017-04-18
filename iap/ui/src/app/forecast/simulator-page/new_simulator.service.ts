import { Injectable } from '@angular/core';


import 'rxjs/add/operator/toPromise';


import {LocalStorageService} from 'angular-2-local-storage';


import { Scenarios } from './mock';


@Injectable()
export class NewSimulatorService {
    private simulation_scenario_id:number = 1;
    private baseline_scenario_id:number = 1;


    constructor(
        public __localStorageService: LocalStorageService
    ) { }


    /*****************************************************
     **************** Load data **************************
     ****************************************************/

    /************************************ Scenario ************************************/
    /* load scenarios from server */
    private __loadScenariosList():Promise<Array<Object>> {
        return Promise.resolve(Scenarios);
    }


    /*****************************************************
     *************** Render data *************************
     ****************************************************/

    /************************************ Scenario ************************************/
    /* render scenarios to component */
    public getScenariosList() {
        let s_list:Object[] = [];
        this.__loadScenariosList().then(
            scenarios => {
                for (let i = 0; i < scenarios.length; i++) {
                    let scenario_item = {
                        'id': scenarios[i]['id'],
                        'name': scenarios[i]['name'],
                    };
                    s_list.push(scenario_item);
                }
            }
        );
        console.log('/* render scenarios to component */', s_list);
        return s_list;
    }

    /* get baseline scenario */
    public getBaselineScenario():Object {
        let b_scenario:Object = {};
        this.__loadScenariosList().then(
            scenarios => {
                for (let i = 0; i < scenarios.length; i++) {
                    if(scenarios[i]['id'] == this.baseline_scenario_id) {
                        b_scenario = {
                            'id': scenarios[i]['id'],
                            'name': scenarios[i]['name'],
                        };
                        console.log(b_scenario);
                        break;
                    }
                }
            }
        );
        return b_scenario;
    }

    /* update baseline scenario */
    public updateBaselineScenario(id: number) {

    }

    /* get simulation scenario */
    public getSimulationScenario():Object {
        let s_scenario:Object = null;
        this.__loadScenariosList().then(
            scenarios => {
                for (let i = 0; i < scenarios.length; i++) {
                    if(scenarios[i]['id'] === this.simulation_scenario_id) {
                        s_scenario = {
                            'id': scenarios[i]['id'],
                            'name': scenarios[i]['name'],
                        };
                        break;
                    }
                }
            }
        );
        return s_scenario;
    }
}
