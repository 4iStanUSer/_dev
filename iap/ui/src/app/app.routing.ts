// import { provideRouter, RouterConfig } from '@angular/router';
//
// import {
//     IndexPageComponent as ForecastIndexPageComponent
// } from './forecast/index-page/';
// import {
//     EditPageComponent as ForecastEditPageComponent
// } from './forecast/edit-page/';
//
//
// export const routes: RouterConfig = [
//     { path: '', pathMatch: 'full', redirectTo: 'forecast' },
//     { path: 'forecast', component: ForecastIndexPageComponent }, //outlet: 'forecast',
//     { path: 'forecast/edit', component: ForecastEditPageComponent } //outlet: 'tree',
// ];
//
// export const APP_ROUTER_PROVIDERS = [
//     provideRouter(routes)
// ];

import { Routes, RouterModule } from '@angular/router';
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
    // { path: '**', component: PageNotFoundComponent }
    { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
    { path: 'dashboard', component: ForecastDashboardCmp }, //outlet: 'forecast',
    { path: 'forecast', component: ForecastIndexPageComponent }, //outlet: 'forecast',
    // { path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' }
    { path: 'forecast/edit', component: ForecastEditPageComponent }, //outlet: 'tree',
    { path: 'forecast/scenarios', component: ForecastScenariosCmp }
];

export const appRoutingProviders: any[] = [

];

export const routing = RouterModule.forRoot(appRoutes); // Lazy Loading -> export const routing: ModuleWithProviders = RouterModule.forRoot(routes);

