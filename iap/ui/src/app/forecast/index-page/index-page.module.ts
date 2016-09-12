import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
    ComponentFactoryService
} from './../../common/service/component-factory.service';
// import { TimeseriesWidgetModule } from './../../common/cmp/timeseries-widget/';
// import { HierarchyWidgetComponent } from './../../common/cmp/hierarchy-widget/';
// import { DropdownComponent } from './../../common/cmp/dropdown/';
// import { DatepickerComponent } from "./../../common/cmp/datepicker/";

import {
    NavagationPanelComponent,
    IndexPageComponent
} from './index-page.component';
import {IndexPageService} from './../service/index-page.service';

@NgModule({
    imports: [
        CommonModule
        // ComponentFactoryModule
        // TimeseriesWidgetModule
    ],
    declarations: [
        // TimeseriesWidgetComponent,
        // HierarchyWidgetComponent,
        // DropdownComponent,
        // DatepickerComponent,
        NavagationPanelComponent,
        IndexPageComponent
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
