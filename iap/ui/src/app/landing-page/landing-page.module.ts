import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LandingPageComponent } from './landing-page.component';
import {FormsModule} from "@angular/forms";
import {CommonServicesModule} from "../common/module/common-services.module";
import { ToolSelectorComponent } from './tool-selector/tool-selector.component';
import {LanguageSelectorComponent} from "./language-selector/language-selector.component";
import { UserMenu } from  "../common/notification/user.components";
import { LoginPageComponent} from "../common/login-page/page/login-page.component";
import {HeaderComponent} from "../common/header-component/header.component";




@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        CommonServicesModule,
    ],
    declarations: [LandingPageComponent, ToolSelectorComponent, LanguageSelectorComponent, HeaderComponent,
        UserMenu, LoginPageComponent],
    exports: [
        LandingPageComponent
    ]
})
export class LandingPageModule { }
