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
import {AuthService} from './common/login-page/auth.service'
import {AppRoutingModule} from './app-routing.module'
import {AppComponent} from './app.component';
import {LoginPageComponent} from "./common/login-page/page/login-page.component"
import {AuthGuard} from
    "./common/login-page/auth.guard"
import {LandingPageComponent} from
    "./common/pages/landing-page/landing-page.component";
import {CommonServicesModule} from
    "./common/module/common-services.module";
import {LandingPageModule} from
    "./landing-page/landing-page.module";
import {NotificationComponent} from
    "./common/notification/notification.component"
import {TestComponent} from
    "./common/notification/test.components"
import {NotificationService} from
    "./common/service/notification.service"

import {MenuWidgetComponent} from "./forecast/menu-widget/menu-widget.component"
import {ForecastComponent} from "./forecast/forecast.component";
import {ForecastModule} from "./forecast/forecast.module";


function authHttpServiceFactory(http: Http, options: RequestOptions) {
  return new AuthHttp(new AuthConfig({
        tokenName: 'token',
        noJwtError:true,
        tokenGetter: (() => localStorage.getItem('token')),
		globalHeaders: [{'Content-Type':'application/json'}]
	}), http, options);
}

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        FormsModule,
        AppRoutingModule,
        CommonServicesModule,
        HttpModule,
        LandingPageModule,
        ForecastModule
    ],
    declarations: [
        AppComponent,
        LandingPageComponent,
        LoginPageComponent,
        TestComponent,
        NotificationComponent,
        MenuWidgetComponent,
        ForecastComponent

    ],
    entryComponents:
        [AppComponent, LoginPageComponent, TestComponent, MenuWidgetComponent],

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
    bootstrap: [AppComponent]

})

export class AppModule {
}
