import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';

import {LandingPageComponent} from "./common/pages/landing-page/landing-page.component";

@NgModule({
    imports: [
        RouterModule.forRoot([
            {path: '', pathMatch: 'full', redirectTo: 'landing'},
            {path: 'landing', component: LandingPageComponent}
        ])
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {
}
