import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {
    CommonModule,
    LocationStrategy,
    HashLocationStrategy
} from '@angular/common';
import { AuthHttp, AuthConfig } from 'angular2-jwt';
import { Http, HttpModule, RequestOptions} from '@angular/http';
import {BrowserModule} from '@angular/platform-browser';
import {AuthService} from './login-page/auth.service'
import {AppRoutingModule} from './app-routing.module'
import {AppComponent} from './app.component';
import {LoginPageComponent} from "./login-page/login-page.component"
import {AuthGuard} from
    "./login-page/auth.guard"
import {LandingPageComponent} from
    "./common/pages/landing-page/landing-page.component";
import {CommonServicesModule} from
    "./common/module/common-services.module";
import {LandingPageModule} from
    "./landing-page/landing-page.module";
import {NotificationComponent} from
    "./login-page/notification/notification.component"
import {TestComponent} from
    "./login-page/notification/test.components"
import {NotificationService} from
    "./login-page/notification/notification.service"
import { ReactiveFormsModule } from '@angular/forms';


function authHttpServiceFactory(http: Http, options: RequestOptions) {
  return new AuthHttp(new AuthConfig({
    tokenName: 'token',
		tokenGetter: (() => localStorage.getItem('token')),
		globalHeaders: [{'Content-Type':'application/json'}],
	}), http, options);
}

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        AppRoutingModule,
        CommonServicesModule,
        HttpModule,
        LandingPageModule
    ],
    declarations: [
        AppComponent,
        LandingPageComponent,
        LoginPageComponent,
        TestComponent,
        NotificationComponent,
    ],
    providers: [
        {
            provide: LocationStrategy, useClass: HashLocationStrategy
        },
        AuthService,
        NotificationService,
        AuthGuard,
        {
            provide: AuthHttp,
            useFactory: authHttpServiceFactory,
            deps: [Http, RequestOptions]
        }
    ],
    entryComponents: [
        AppComponent
    ],
    bootstrap: [AppComponent]

})

export class AppModule {
}
