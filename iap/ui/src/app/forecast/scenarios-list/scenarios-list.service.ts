import { Injectable }    from '@angular/core';
import 'rxjs/add/operator/toPromise';
import {AjaxService} from "../../common/service/ajax.service";


const  USER_PERMISSION = {finalize: 'True', duplicate: 'True', delete: 'True', edit: 'True',
    create: 'True', share: 'True'};

@Injectable()
export class ScenariosListComponentService {

    private getScenarioPage = '/forecast/get_scenario_page';

    constructor(private req: AjaxService) { }

    getScenariosList() {
        this.req.post({
            url_id: this.getScenarioPage,
            data: {'filter': {}},
        }).subscribe((data) => {
            console.log('*****getScenariosList', data.data);
            return data.data;
        });
    }

    getUserPermissions(): Promise<any> {
      return Promise.resolve(USER_PERMISSION);
    }

    getScenario(scenario_id: number) {
        return null;
        //return this.getScenariosList().then(list => list.find(item => item.id == scenario_id));
    }

    modifyFavorit(scenario_id: number) {
        let scenario = this.getScenario(scenario_id);
        scenario.isFavorite = !scenario.isFavorite;
        // Send to backend
    }
}
