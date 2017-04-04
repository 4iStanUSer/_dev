import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';
import {AuthGuard} from "./common/login-page/auth.guard";
import {ForecastComponent} from "./forecast/forecast.component";
import {LandingPageComponent} from "./landing-page/landing-page.component";

@NgModule({
    imports: [
        RouterModule.forRoot([
            {
                path:'',
                pathMatch: 'full',
                redirectTo:'/landing'
            },
             {
                path: 'forecast',
                component: ForecastComponent,
                canActivate: [AuthGuard],
            },
            {
                path:'landing',
                component: LandingPageComponent,
            },

        ])
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {
}
