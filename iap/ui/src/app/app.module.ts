import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {
    CommonModule,
    Location,
    LocationStrategy,
    HashLocationStrategy,
    PathLocationStrategy,
} from '@angular/common';
import { AuthHttp, AuthConfig } from 'angular2-jwt';
import { Http, HttpModule, RequestOptions} from '@angular/http';
import {BrowserModule} from '@angular/platform-browser';
import {AuthService} from './common/login-page/auth.service'
import {AppRoutingModule} from './app-routing.module'
import {AppComponent} from './app.component';
import {ConfigurationService} from "./common/service/configuration.service";
import {AuthGuard} from
    "./common/login-page/auth.guard"
import {CommonServicesModule} from
    "./common/module/common-services.module";
import {LandingPageModule} from
    "./landing-page/landing-page.module";
import {NotificationComponent} from
    "./common/notification/notification.component"
import {NotificationService} from
    "./common/service/notification.service"
import {MenuWidgetComponent} from "./forecast/menu-widget/menu-widget.component"
import {ForecastComponent} from "./forecast/forecast.component";
import {ForecastModule} from "./forecast/forecast.module";

export function authHttpServiceFactory(http: Http, options: RequestOptions) {
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
        NotificationComponent,
        MenuWidgetComponent,
        ForecastComponent

    ],
    entryComponents:
        [AppComponent],

    providers: [
        Location,
        {provide: LocationStrategy, useClass: HashLocationStrategy},
        AuthService,
        NotificationService,
        ConfigurationService,
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
