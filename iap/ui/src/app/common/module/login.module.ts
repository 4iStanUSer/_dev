import {NgModule} from '@angular/core';
import {LoginWidgetComponent} from "../cmp/login-widget/login-widget.component";
import {LoginService} from "../service/login.service";


@NgModule({
    declarations: [
        LoginWidgetComponent
    ],
    providers: [
        LoginService,
    ]
})
export class LoginModule {

}
