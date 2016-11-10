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

import {CommonServicesModule} from "./common/module/common-services.module";

import {ForecastModule} from "./forecast/forecast.module";

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
        LandingPageComponent
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
