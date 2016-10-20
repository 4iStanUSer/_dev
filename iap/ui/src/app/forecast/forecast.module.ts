import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

import {CommonServicesModule} from "../common/module/common-services.module";
import {DataManagerService} from "./dashboard/data-manager.service";

import {ForecastRoutingModule} from "./forecast-routing.module";
import {ForecastComponent} from "./forecast.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {ScenariosListComponent} from "./scenarios-list/scenarios-list.component";
import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";

import {ChartModule} from '../common/module/chart/';
import {DonutChartComponent} from "../common/cmp/donut-chart/donut-chart.component";
import {BarChartComponent} from "../common/cmp/bar-chart/bar-chart.component";
import {WaterfallChartComponent} from "../common/cmp/waterfall-chart/waterfall-chart.component";
import {AccordionTableComponent} from "../common/cmp/accordion-table/accordion-table.component";
import {SwitchSelectorComponent} from "../common/cmp/switch-selector/switch-selector.component";


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ForecastRoutingModule,

        CommonServicesModule,
        ChartModule,
        // HierarchyWidgetModule,
        // DropdownModule,
        // TimeseriesWidgetModule,
        // ForecastIndexPageModule,
    ],
    declarations: [
        ForecastComponent,
        DashboardComponent,
        ScenariosListComponent,
        SimulatorPageComponent,

        DonutChartComponent,
        BarChartComponent,
        WaterfallChartComponent,
        AccordionTableComponent,
        SwitchSelectorComponent,
    ],
    providers: [
        DataManagerService,
        CommonServicesModule
    ]
})
export class ForecastModule {
}
