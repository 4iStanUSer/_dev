import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from "@angular/forms";

import {AlertComponent} from "./alert/alert.component";
import {LoginFormComponent} from "./login-form/login-form.component";
import {LoginComponent} from "./login.component";
import {AlertService} from "./services/alert.service";
import {AjaxService} from "../../service/ajax.service";

@NgModule({
    imports: [
        CommonModule,
        FormsModule
    ],
    declarations: [
        AlertComponent,
        LoginFormComponent,
        LoginComponent
    ],
    exports: [
        LoginComponent
    ],
    providers: [
        AlertService,
        AjaxService
    ]
})
export class LoginModule {
}
