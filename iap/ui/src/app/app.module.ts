import {BrowserModule} from '@angular/platform-browser';
import {NgModule, ApplicationRef} from '@angular/core';
import {
    CommonModule, LocationStrategy,
    HashLocationStrategy
} from '@angular/common';
import {RouterModule} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {HttpModule, JsonpModule} from '@angular/http';
import {AppComponent} from './app.component';

import {
    routing,
    appRoutingProviders
} from './app.routing';

import {MenuWidgetComponent} from './common/cmp/menu-widget/';
import {HierarchyWidgetComponent} from './common/cmp/hierarchy-widget/';
import {TimeseriesWidgetComponent} from './common/cmp/timeseries-widget/';
import {DropdownComponent} from './common/cmp/dropdown/';
import {AjaxService} from './common/service/ajax.service';
import {LoadingService} from './common/service/loading.service';
import {ComponentFactoryService} from './common/service/component-factory.service';
import {IndexPageService} from "./forecast/service/index-page.service";
import {IndexPageComponent as ForecastIndexPageCmp} from "./forecast/index-page/";
import {EditPageComponent as ForecastEditPageCmp} from "./forecast/edit-page/";

@NgModule({
    imports: [
        BrowserModule,
        RouterModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        routing
    ],
    declarations: [
        AppComponent,
        MenuWidgetComponent,
        ForecastIndexPageCmp,
        ForecastEditPageCmp,

        HierarchyWidgetComponent,
        DropdownComponent,
        TimeseriesWidgetComponent
    ],
    providers: [
        {provide: LocationStrategy, useClass: HashLocationStrategy},
        appRoutingProviders,
        IndexPageService,
        AjaxService,
        LoadingService,
        ComponentFactoryService
    ],
    entryComponents: [
        AppComponent,
        HierarchyWidgetComponent,
        DropdownComponent,
        TimeseriesWidgetComponent
    ],
    bootstrap: [AppComponent]
})
export class AppModule {

}
