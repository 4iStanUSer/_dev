import {NgModule}       from '@angular/core';
import {RouterModule}   from '@angular/router';

import {AuthGuard} from "../common/module/login/auth-guard";

import {ForecastComponent} from "./forecast.component";
import {DashboardComponent} from "./dashboard/dashboard.component";

import {ScenariosComponent} from "./scenarios/scenarios.component";
import {ScenariosListComponent} from "./scenarios/scenarios-list/scenarios-list.component";

import {UsersComponent} from "./users/users.component";
import {UsersListComponent} from "./users/users-list/users-list.component";

import {NewScenarioComponent} from "./scenarios/new-scenario/new-scenario.component";
import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";
import {GeneralComponent} from "./dashboard/general/general.component";
import {DriverSummaryComponent} from "./dashboard/driver-summary/driver-summary.component";
import {DriverDetailComponent} from "./dashboard/driver-detail/driver-detail.component";
import {LandingPageComponent} from "./landing-page/landing-page.component"
//for now this page is used for development & minor components testing
import {EditPageComponent} from "./edit-page/edit-page.component";


@NgModule({
    imports: [
        RouterModule.forChild([
            {
                path: 'forecast',
                component: ForecastComponent,
                canActivate: [AuthGuard],
                canActivateChild: [AuthGuard],
                // canDeactivate: [CanDeactivateGuard]
                children: [
                    {
                        path: '',
                        redirectTo: 'landing',
                        pathMatch: 'full',
                    },
                    {
                        path: 'landing',
                        component: LandingPageComponent
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
                            },
                            {
                                path: 'driver-details',
                                component: DriverDetailComponent
                            }
                        ]
                    },
                    {
                        path: 'scenarios',
                        component: ScenariosComponent,

                        children: [
                            {
                                path: '',
                                redirectTo: 'scenarios-list',
                                pathMatch: 'full'
                            },
                            {
                                path: 'scenarios-list',
                                component: ScenariosListComponent,
                            },
                            {
                                path: 'new-scenario',
                                component: NewScenarioComponent,
                            },
                            {
                                path: 'edit-scenario/:id',
                                component: NewScenarioComponent,
                            }
                        ]
                    },
                    {
                        path: 'users',
                        component: UsersComponent,

                        children: [
                            {
                                path: '',
                                redirectTo: 'users-list',
                                pathMatch: 'full'
                            },
                            {
                                path: 'users-list',
                                component: UsersListComponent,
                            },
                        ]
                    },
                    {
                        path: 'simulator',
                        component: SimulatorPageComponent
                    },
                    {
                        path: 'edit-page',
                        component: EditPageComponent
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
