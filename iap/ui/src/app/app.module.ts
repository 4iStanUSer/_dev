import {
    CommonModule,
    LocationStrategy,
    HashLocationStrategy,
    Location
} from '@angular/common';
import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {HttpModule, JsonpModule} from '@angular/http';

import {AppComponent} from './app.component';
import {routing, appRoutingProviders} from './app.routing';

/*Dashboard*/
import {DashboardComponent} from './forecast/dashboard/dashboard.component';
import {
    DataManagerService as DashboardDM
} from './forecast/dashboard/data-manager.service';
/*.Dashboard*/

/*Decide about below*/
import {MenuWidgetComponent} from './common/cmp/menu-widget/';
import {AjaxService} from './common/service/ajax.service';
import {LoadingService} from './common/service/loading.service';
import {StaticDataService} from "./common/service/static-data.service";
import {StateService} from "./common/service/state.service";

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
import {AccordionTableComponent} from "./common/cmp/accordion-table/accordion-table.component";
import {SwitchSelectorComponent} from "./common/cmp/switch-selector/switch-selector.component";
/*.Charts section*/

/*Pipes section*/
import {FilterListPipe} from "./common/pipes/filter-list.pipe";

/*.Pipes section*/
/*Login section*/
import {AlertService} from "./common/module/login/services/alert.service";
import {LoginComponent} from "./common/module/login/login.component";
import {LoginFormComponent} from "./common/module/login/login-form/login-form.component";
import {AlertComponent} from "./common/module/login/alert/alert.component";
/*Login section*/

@NgModule({
    imports: [
        BrowserModule,
        CommonModule,
        RouterModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        routing,

        /*Decide about below*/
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
        /*Decide about below*/
        FilterListPipe,
        DonutChartComponent,
        BarChartComponent,
        WaterfallChartComponent,
        AccordionTableComponent,
        SwitchSelectorComponent,

        MenuWidgetComponent,
        ForecastEditPageCmp,
        ScenariosListComponent,

        AlertComponent,
        LoginFormComponent,
        LoginComponent
    ],
    providers: [
        {provide: LocationStrategy, useClass: HashLocationStrategy},
        appRoutingProviders,
        Location,

        /*Decide about below*/
        DashboardDM,
        AjaxService,
        LoadingService,
        ComponentFactoryService,
        StaticDataService,
        StateService,
        AlertService
    ],
    entryComponents: [
        AppComponent,
        /*Decide about below*/
        HierarchyWidgetComponent,
        DropdownComponent,
        TimeseriesWidgetComponent
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
