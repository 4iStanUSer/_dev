import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TimeseriesWidgetComponent } from './timeseries-widget.component';

@NgModule({
    imports: [
        CommonModule,
        FormsModule
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
