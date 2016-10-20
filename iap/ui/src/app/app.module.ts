import {
    CommonModule,
    LocationStrategy,
    HashLocationStrategy
} from '@angular/common';
import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';

import {AppComponent} from './app.component';
import {AppRoutingModule} from "./app-routing.module";

import {LandingPageComponent} from "./common/pages/landing-page/landing-page.component";
import {MenuWidgetComponent} from './common/cmp/menu-widget/';
import {CommonServicesModule} from "./common/module/common-services.module";
import {ForecastModule} from "./forecast/forecast.module";

/*Login section*/
// import {AlertService} from "./common/module/login/services/alert.service";
// import {LoginComponent} from "./common/module/login/login.component";
// import {LoginFormComponent} from "./common/module/login/login-form/login-form.component";
// import {AlertComponent} from "./common/module/login/alert/alert.component";
/*Login section*/

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        FormsModule,
        AppRoutingModule,
        CommonServicesModule,
        ForecastModule
    ],
    declarations: [
        AppComponent,
        LandingPageComponent,
        MenuWidgetComponent
    ],
    providers: [
        {provide: LocationStrategy, useClass: HashLocationStrategy},
    ],
    entryComponents: [
        AppComponent
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
