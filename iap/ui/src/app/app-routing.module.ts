import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';

import {LandingPageComponent} from "./common/pages/landing-page/landing-page.component";
import {AuthGuard} from "./common/module/login/auth-guard";

@NgModule({
    imports: [
        RouterModule.forRoot([
            {path: '', pathMatch: 'full', redirectTo: 'landing'},
            {
                path: 'landing',
                component: LandingPageComponent,
                canActivate: [AuthGuard],
            }
        ])
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {
}
