import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TimeseriesWidgetComponent } from './timeseries-widget.component';

@NgModule({
    imports: [
        CommonModule,
    ],
    declarations: [
        TimeseriesWidgetComponent
    ],
    providers: [
    ],
    exports: [
        TimeseriesWidgetComponent
    ]
})
export class TimeseriesWidgetModule { }
