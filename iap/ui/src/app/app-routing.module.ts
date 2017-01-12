import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';

//import {LandingPageComponent} from "./common/pages/landing-page/landing-page.component";
import {AuthGuard} from "./common/module/login/auth-guard";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {LoginComponent} from "./common/module/login/login/login.component";
@NgModule({
    imports: [
        RouterModule.forRoot([
            /*
            {
                path: '',
                pathMatch: 'full',
                redirectTo: '/landing',
            },

            {
                path: 'landing',
                component: LandingPageComponent,
                canActivate: [AuthGuard],
            }
            */
            {
                path:'',
                pathMatch: 'full',
                redirectTo:'/login'
            },
            {
                path: 'landing',
                component: LoginComponent,
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
