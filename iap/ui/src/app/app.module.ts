import {
    CommonModule,
    LocationStrategy,
    HashLocationStrategy
} from '@angular/common';
import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {HttpModule, JsonpModule} from '@angular/http';

import {AppComponent} from './app.component';
import {routing, appRoutingProviders} from './app.routing';
import {DashboardComponent} from "./forecast/dashboard/dashboard.component";

/*Decide about bottom*/
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

/*Charts section*/
import {ChartModule} from './common/module/chart/';
import {DonutChartComponent} from "./common/cmp/donut-chart/donut-chart.component";
import {BarChartComponent} from "./common/cmp/bar-chart/bar-chart.component";
import {WaterfallChartComponent} from "./common/cmp/waterfall-chart/waterfall-chart.component";
/*.Charts section*/

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        RouterModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        routing,

        /*Decide about bottom*/
        ChartModule,
        HierarchyWidgetModule,
        DropdownModule,
        TimeseriesWidgetModule,
        ForecastIndexPageModule,
        // ScenariosListModule
    ],
    declarations: [
        AppComponent,
        DashboardComponent,
        /*Decide about bottom*/
        DonutChartComponent,
        BarChartComponent,
        WaterfallChartComponent,

        MenuWidgetComponent,
        ForecastEditPageCmp,
        ScenariosListComponent,
    ],
    providers: [
        {provide: LocationStrategy, useClass: HashLocationStrategy},
        appRoutingProviders,
        /*Decide about bottom*/
        AjaxService,
        LoadingService,
        ComponentFactoryService
    ],
    entryComponents: [
        AppComponent,
        /*Decide about bottom*/
        HierarchyWidgetComponent,
        DropdownComponent,
        TimeseriesWidgetComponent
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
