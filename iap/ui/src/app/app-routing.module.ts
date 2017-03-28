import {NgModule}     from '@angular/core';
import {RouterModule} from '@angular/router';
import {AuthGuard} from "./login-page/auth.guard";
import {LandingPageComponent} from "./landing-page/landing-page.component";
import {LoginPageComponent} from "./login-page/login-page.component";
import {TestComponent} from './login-page/notification/test.components'
@NgModule({
    imports: [
        RouterModule.forRoot([
            {
                path:'',
                pathMatch: 'full',
                redirectTo:'/login_page'
            },
            {
                path: 'login_page',
                component: LoginPageComponent,
            },
             {
                path: 'landing',
                component: LandingPageComponent,
                canActivate: [AuthGuard],
            },
            {
                path:'notification',
                component: TestComponent,
            }
        ])
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {
}
