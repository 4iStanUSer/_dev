import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
    ComponentFactoryService
} from './../../common/service/component-factory.service';
import { DonutChartComponent } from './../../common/cmp/donut-chart/donut-chart.component';
// import { TimeseriesWidgetModule } from './../../common/cmp/timeseries-widget/';
// import { HierarchyWidgetComponent } from './../../common/cmp/hierarchy-widget/';
// import { DropdownComponent } from './../../common/cmp/dropdown/';
// import { DatepickerComponent } from "./../../common/cmp/datepicker/";

import {
    NavagationPanelComponent,
    IndexPageComponent
} from './index-page.component';
import {IndexPageService} from './../service/index-page.service';


// import { ChartModule } from './../../common/module/chart/';


@NgModule({
    imports: [
        CommonModule,
        // ComponentFactoryModule
        // TimeseriesWidgetModule

        // ChartModule
    ],
    declarations: [
        // TimeseriesWidgetComponent,
        // HierarchyWidgetComponent,
        // DropdownComponent,
        // DatepickerComponent,
        NavagationPanelComponent,
        IndexPageComponent,
        // DonutChartComponent
    ],
    exports: [
        IndexPageComponent
    ],
    providers: [
        IndexPageService,
        ComponentFactoryService
    ]
})
export class IndexPageModule {
}
