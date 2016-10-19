import { Routes, RouterModule } from '@angular/router';

import {LandingPageComponent} from "./common/pages/landing-page/landing-page.component";

import {
    IndexPageComponent as ForecastIndexPageComponent
} from './forecast/index-page/index-page.component';
import {
    EditPageComponent as ForecastEditPageComponent
} from './forecast/edit-page/';
import {
    ScenariosListComponent as ForecastScenariosCmp
} from './forecast/scenarios-list/scenarios-list.component';
import {
    DashboardComponent as ForecastDashboardCmp
} from './forecast/dashboard/dashboard.component';
import {LoginComponent} from "./common/module/login/login.component";


const appRoutes: Routes = [
    // { path: 'crisis-center', component: CrisisCenterComponent },
    // {
    // path: 'heroes',
    // component: HeroListComponent,
    // data: {
    // title: 'Heroes List'
    // }
    // },
    // { path: 'hero/:id', component: HeroDetailComponent },
    // { path: '**', component: PageNotFoundComponent },
    // { path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' }
    { path: '', pathMatch: 'full', redirectTo: 'landing' },
    { path: 'landing', component: LandingPageComponent }, //outlet: 'forecast',

    // TODO TO BE MOVED  into forecast module (VL)
    { path: 'dashboard', component: ForecastDashboardCmp }, //outlet: 'forecast',
    { path: 'forecast', component: ForecastDashboardCmp }, //outlet: 'forecast',
    // { path: 'forecast', component: ForecastIndexPageComponent }, //outlet: 'forecast',
    { path: 'login', component: LoginComponent }, //outlet: 'forecast',
    { path: 'forecast/edit', component: ForecastEditPageComponent }, //outlet: 'tree',
    { path: 'forecast/scenarios', component: ForecastScenariosCmp }
];

export const appRoutingProviders: any[] = [

];

export const routing = RouterModule.forRoot(appRoutes); // Lazy Loading -> export const routing: ModuleWithProviders = RouterModule.forRoot(routes);

