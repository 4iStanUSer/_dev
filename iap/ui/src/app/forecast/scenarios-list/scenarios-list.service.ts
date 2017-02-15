import { Injectable } from '@angular/core';

const  SCENARIOS = [
    {id: 11, isFavorite: true, name: 'Mr. Nice', author: 'Mr. Nice', shared: 'True',
        description: 'Mr. Nice', modify_date: '2017-02-10 14:00:13.990018', status: 'Draft',
        scenario_permission: ['share','copy','delete']
    },
    {id: 12, isFavorite: false, name: 'Mr. Nice', author: 'Mr. Nice2', shared: 'False',
        description: 'Mr. Nice2', modify_date: '2017-02-10 14:00:13.990018', status: 'draft',
        scenario_permission: ['share','change status','delete','edit']
    },
    {id: 13, isFavorite: false, name: 'Mr. Nice', author: 'Mr. Nice2', shared: 'True',
        description: 'Mr. Nice2', modify_date: '2017-02-10 14:00:13.990018', status: 'Final',
        scenario_permission: ['change status','copy']
    },
    {id: 14, isFavorite: true, name: 'Mr. Nice', author: 'Mr. Nice', shared: 'False',
        description: 'Mr. Nice', modify_date: '2017-02-10 14:00:13.990018', status: 'Final',
        scenario_permission: ['delete','edit']
    },
];

const  USER_PERMISSION = {finalize: 'True', duplicate: 'True', delete: 'True', edit: 'True',
    create: 'True', share: 'True'};

@Injectable()
export class ScenariosListComponentService {
    getScenariosList(): Promise<any[]> {
      return Promise.resolve(SCENARIOS);
    }

    getUserPermissions(): Promise<any> {
      return Promise.resolve(USER_PERMISSION);
    }

    getScenario(scenario_id: number) {
        return this.getScenariosList().then(list => list.find(item => item.id == scenario_id));
    }

    modifyFavorit(scenario_id: number) {
        let scenario = this.getScenario(scenario_id);
        scenario.isFavorite = !scenario.isFavorite;
        // Send to backend
    }
}
