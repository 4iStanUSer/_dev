import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from "@angular/forms";

import {CommonServicesModule} from "../common-services.module";

import {LoginRoutingModule} from "./login-routing.module";
import {LoginComponent} from "./login/login.component";

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        LoginRoutingModule,
        CommonServicesModule // TODO Review
    ],
    declarations: [
        LoginComponent
    ],
    exports: [],
    providers: []
})
export class LoginModule {
}
