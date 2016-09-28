import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {
    CommonModule,
    LocationStrategy,
    HashLocationStrategy
} from '@angular/common';
import {RouterModule} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {HttpModule, JsonpModule} from '@angular/http';

import {AppComponent} from './app.component';
import {routing, appRoutingProviders} from './app.routing';
import {MenuWidgetComponent} from './common/cmp/menu-widget/';
import {AjaxService} from './common/service/ajax.service';
import {LoadingService} from './common/service/loading.service';

import {EditPageComponent as ForecastEditPageCmp} from './forecast/edit-page/';
import {IndexPageModule as ForecastIndexPageModule} from './forecast/index-page/';

import {ComponentFactoryService} from './common/service/component-factory.service';
import {
    HierarchyWidgetModule,
    HierarchyWidgetComponent
} from './common/cmp/hierarchy-widget/';
import {DropdownModule, DropdownComponent} from './common/cmp/dropdown/';
import {
    TimeseriesWidgetModule,
    TimeseriesWidgetComponent
} from './common/cmp/timeseries-widget/';
import {ScenariosListComponent} from './forecast/scenarios-list/';


@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        RouterModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        routing,

        HierarchyWidgetModule,
        DropdownModule,
        TimeseriesWidgetModule,

        ForecastIndexPageModule,
        // ScenariosListModule
    ],
    declarations: [
        AppComponent,
        MenuWidgetComponent,
        ForecastEditPageCmp,
        ScenariosListComponent
    ],
    providers: [
        {provide: LocationStrategy, useClass: HashLocationStrategy},
        appRoutingProviders,
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
