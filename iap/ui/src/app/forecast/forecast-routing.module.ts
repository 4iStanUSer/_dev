import {NgModule}       from '@angular/core';
import {RouterModule}   from '@angular/router';

import {ForecastComponent} from "./forecast.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {ScenariosListComponent} from "./scenarios-list/scenarios-list.component";
import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";

@NgModule({
    imports: [
        RouterModule.forChild([
            {
                path: 'forecast',
                component: ForecastComponent,
                children: [
                    {
                        path: '',
                        redirectTo: '/forecast/dashboard',
                        pathMatch: 'full'
                    },
                    {
                        path: 'dashboard',
                        component: DashboardComponent
                    },
                    {
                        path: 'scenarios',
                        component: ScenariosListComponent
                    },
                    {
                        path: 'simulator',
                        component: SimulatorPageComponent
                    }
                ]
            }
        ])
    ],
    exports: [
        RouterModule
    ]
})
export class ForecastRoutingModule {
}
