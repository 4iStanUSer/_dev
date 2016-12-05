import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page.component';
import {FormsModule} from "@angular/forms";
import {CommonServicesModule} from "../common/module/common-services.module";
import { ToolSelectorComponent } from './tool-selector/tool-selector.component';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        CommonServicesModule
    ],
    declarations: [LandingPageComponent, ToolSelectorComponent],
    exports: [
        LandingPageComponent
    ]
})
export class LandingPageModule { }
