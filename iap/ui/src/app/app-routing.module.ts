import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';
import {AuthGuard} from "./common/login-page/auth.guard";
import {LoginPageComponent} from "./common/login-page/page/login-page.component";
import {TestComponent} from './common/notification/test.components';
import {LandingPageComponent} from  './landing-page/landing-page.component';
import {ForecastComponent} from "./forecast/forecast.component";

@NgModule({
    imports: [
        RouterModule.forRoot([
            {
                path:'',
                pathMatch: 'full',
                redirectTo:'/landing'
            },
            {
                path: 'login_page',
                component: LoginPageComponent,
            },
             {
                path: 'landing',
                component: LandingPageComponent,
            },
             {
                path: 'forecast',
                component: ForecastComponent,
                canActivate: [AuthGuard],
            },
            {
                path:'notification',
                component: TestComponent,
                canActivate: [AuthGuard],
            },

        ])
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {
}
