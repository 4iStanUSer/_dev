import {NgModule}       from '@angular/core';
import {RouterModule}   from '@angular/router';

import {AuthGuard} from "../common/module/login/auth-guard";

import {ForecastComponent} from "./forecast.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {ScenariosListComponent} from "./scenarios-list/scenarios-list.component";
import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";
import {GeneralComponent} from "./dashboard/general/general.component";
import {DriverSummaryComponent} from "./dashboard/driver-summary/driver-summary.component";
import {DriverDetailComponent} from "./dashboard/driver-detail/driver-detail.component";


@NgModule({
    imports: [
        RouterModule.forChild([
            {
                path: 'forecast',
                component: ForecastComponent,
                canActivate: [AuthGuard],
                // canActivateChild: [AuthGuard],
                children: [
                    {
                        path: '',
                        redirectTo: 'dashboard',
                        pathMatch: 'full',
                    },
                    {
                        path: 'dashboard',
                        component: DashboardComponent,

                        children: [
                            {
                                path: '',
                                redirectTo: 'general',
                                pathMatch: 'full'
                            },
                            {
                                path: 'general',
                                component: GeneralComponent
                            },
                            {
                                path: 'driver-summary',
                                component: DriverSummaryComponent,
                                //canDeactivate: [CanDeactivateGuard]
                            },
                            {
                                path: 'driver-details',
                                component: DriverDetailComponent
                            }
                        ]
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
