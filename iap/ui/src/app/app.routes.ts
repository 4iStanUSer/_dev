import { provideRouter, RouterConfig } from '@angular/router';

import {
    IndexPageComponent as ForecastIndexPageComponent
} from './forecast/index-page/';
import {
    EditPageComponent as ForecastEditPageComponent
} from './forecast/edit-page/';


export const routes: RouterConfig = [
    { path: '', pathMatch: 'full', redirectTo: 'forecast' },
    { path: 'forecast', component: ForecastIndexPageComponent }, //outlet: 'forecast', 
    { path: 'forecast/edit', component: ForecastEditPageComponent } //outlet: 'tree',
];

export const APP_ROUTER_PROVIDERS = [
    provideRouter(routes)
];