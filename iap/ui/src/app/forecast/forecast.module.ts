import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import {CommonServicesModule} from "../common/module/common-services.module";
import {ForecastRoutingModule} from "./forecast-routing.module";

import {ChartModule} from '../common/module/chart/';
import {DonutChartComponent} from "../common/cmp/donut-chart/donut-chart.component";
import {BarChartComponent} from "../common/cmp/bar-chart/bar-chart.component";
import {WaterfallChartComponent} from "../common/cmp/waterfall-chart/waterfall-chart.component";
import {TimeSelectorComponent} from '../common/cmp/time-selector/time-selector.component';
import {RangeSliderComponent} from "../common/cmp/time-selector/range-slider/range-slider.component";
import { ValueEditPopupComponent } from "../common/cmp/value-edit-popup/value-edit-popup.component";
import { TableComponent } from "../common/cmp/table/table.component";

import {DashboardComponent} from "./dashboard/dashboard.component";
import {DataManagerService} from "./dashboard/data-manager.service";

import {SimulatorPageComponent} from "./simulator-page/simulator-page.component";
import {SimulatorPageDataManagerService} from "./simulator-page/simulator-page-data-manager.service";

import {ForecastComponent} from "./forecast.component";
import {ScenariosComponent} from "./scenarios/scenarios.component";
import {ScenarioService} from "./scenarios/scenario.service";
import {ScenariosListComponent} from "./scenarios/scenarios-list/scenarios-list.component";
import {NewScenarioComponent} from "./scenarios/new-scenario/new-scenario.component";

import {UsersComponent} from "./users/users.component";
import {UsersListComponent} from "./users/users-list/users-list.component";

// import {SelectorsComponent} from './dashboard/selectors/selectors.component';
// import {FlatSelectorComponent} from './dashboard/selectors/flat-selector/flat-selector.component';
// import {HierarchicalSelectorComponent} from './dashboard/selectors/hierarchical-selector/hierarchical-selector.component';
// import {RegionSelectorComponent} from './dashboard/selectors/region-selector/region-selector.component';

import {GeneralComponent} from './dashboard/general/general.component';
import {DriverDetailComponent} from './dashboard/driver-detail/driver-detail.component';
import {DriverSummaryComponent} from './dashboard/driver-summary/driver-summary.component';
import {InsightsComponent} from './dashboard/insights/insights.component';

import {ButtonsGroupComponent} from './../common/cmp/buttons-group/buttons-group.component';
import {TableWidgetComponent} from "../common/cmp/table-widget/table-widget.component";
import { MenuWidgetComponent } from './menu-widget/menu-widget.component';
import { LanguageSelectorComponent } from './language-selector/language-selector.component';

import { LandingPageComponent } from './landing-page/landing-page.component';
import { LandingPageService } from './landing-page/landing-page.service';

import {SelectorsComponent} from "./selectors/selectors.component";
import {FlatSelectorComponent} from "./selectors/flat-selector/flat-selector.component";
import {HierarchicalSelectorComponent} from "./selectors/hierarchical-selector/hierarchical-selector.component";
import {RegionSelectorComponent} from "./selectors/region-selector/region-selector.component";
//for now this page is used for development & minor components testing
import {EditPageComponent} from "./edit-page/edit-page.component";
import { MyDateRangePickerModule } from 'mydaterangepicker';
import { SelectorsWrapperComponent } from './selectors-wrapper/selectors-wrapper.component';

import { MultiselectDropdownModule } from 'angular-2-dropdown-multiselect';

// import {SelectorsComponent} from "../common/cmp/selectors/selectors.component";
// import {FlatSelectorComponent} from "../common/cmp/selectors/flat-selector/flat-selector.component";
// import {HierarchicalSelectorComponent} from "../common/cmp/selectors/hierarchical-selector/hierarchical-selector.component";
// import {RegionSelectorComponent} from "../common/cmp/selectors/region-selector/region-selector.component";


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        ForecastRoutingModule,
        CommonServicesModule,
        ChartModule,
        MyDateRangePickerModule,
        MultiselectDropdownModule
    ],
    declarations: [
        ForecastComponent,

        DashboardComponent,
        GeneralComponent,
        DriverDetailComponent,
        DriverSummaryComponent,
        InsightsComponent,
        SelectorsComponent,
        FlatSelectorComponent,
        HierarchicalSelectorComponent,

        ScenariosComponent,
        ScenariosListComponent,
        NewScenarioComponent,
        SimulatorPageComponent,

        UsersComponent,
        UsersListComponent,

        DonutChartComponent,
        BarChartComponent,
        WaterfallChartComponent,

        RangeSliderComponent,
        TimeSelectorComponent,
        RegionSelectorComponent,
        ButtonsGroupComponent,
        TableWidgetComponent,
        MenuWidgetComponent,
        LanguageSelectorComponent,
        LandingPageComponent,

        EditPageComponent,
        ValueEditPopupComponent,
        TableComponent
        SelectorsWrapperComponent
    ],
    providers: [
        CommonServicesModule,
        ScenarioService,
        DataManagerService, // TODO Rename (VL)
        SimulatorPageDataManagerService,
        LandingPageService
    ]
})
export class ForecastModule {
}
