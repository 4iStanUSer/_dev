import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

import {CommonServicesModule} from "../common/module/common-services.module";
import {ForecastRoutingModule} from "./forecast-routing.module";

import {ChartModule} from '../common/module/chart/';
import {DonutChartComponent} from "../common/cmp/donut-chart/donut-chart.component";
import {BarChartComponent} from "../common/cmp/bar-chart/bar-chart.component";
import {WaterfallChartComponent} from "../common/cmp/waterfall-chart/waterfall-chart.component";
import {AccordionTableComponent} from "../common/cmp/accordion-table/accordion-table.component";
import {SwitchSelectorComponent} from "../common/cmp/switch-selector/switch-selector.component";
import {TimeSelectorComponent} from '../common/cmp/time-selector/time-selector.component';
import {RangeSliderComponent} from "../common/cmp/time-selector/range-slider/range-slider.component";

import {DashboardComponent} from "./dashboard/dashboard.component";
import {DataManagerService} from "./dashboard/data-manager.service";

import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";
import {SimulatorPageDataManagerService} from "./simulator-page/simulator-page-data-manager.service";

import {ForecastComponent} from "./forecast.component";
import {ScenariosListComponent} from "./scenarios-list/scenarios-list.component";

import {ForecastSectionComponent} from './dashboard/forecast-section/forecast-section.component';
import {SelectorsComponent} from './dashboard/selectors/selectors.component';
import {FlatSelectorComponent} from './dashboard/selectors/flat-selector/flat-selector.component';
import {HierarchicalSelectorComponent} from './dashboard/selectors/hierarchical-selector/hierarchical-selector.component';

import {GeneralComponent} from './dashboard/general/general.component';
import {DriverDetailComponent} from './dashboard/driver-detail/driver-detail.component';
import {DriverSummaryComponent} from './dashboard/driver-summary/driver-summary.component';
import {InsightsComponent} from './dashboard/insights/insights.component';
import {RegionSelectorComponent} from './dashboard/selectors/region-selector/region-selector.component';
import {ButtonsGroupComponent} from './../common/cmp/buttons-group/buttons-group.component';

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
        GeneralComponent,
        DriverDetailComponent,
        DriverSummaryComponent,
        InsightsComponent,
        ForecastSectionComponent,
        SelectorsComponent,
        FlatSelectorComponent,
        HierarchicalSelectorComponent,

        ScenariosListComponent,
        SimulatorPageComponent,

        DonutChartComponent,
        BarChartComponent,
        WaterfallChartComponent,
        AccordionTableComponent,
        SwitchSelectorComponent,

        RangeSliderComponent,
        TimeSelectorComponent,
        RegionSelectorComponent,
        ButtonsGroupComponent
    ],
    providers: [
        CommonServicesModule,

        DataManagerService, // TODO Rename (VL)
        SimulatorPageDataManagerService
    ]
})
export class ForecastModule {
}
