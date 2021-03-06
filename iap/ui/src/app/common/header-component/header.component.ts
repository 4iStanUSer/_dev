import {Component, AfterViewInit, ComponentFactoryResolver, ViewChild, ViewContainerRef, ComponentRef} from '@angular/core';
import { UserMenu } from '../notification/user.components';
import { LoginPageComponent } from '../login-page/page/login-page.component'
import { AuthService } from '../../common/login-page/auth.service';
import {ConfigurationService} from "../service/configuration.service";
@Component({
    selector: 'header',
    templateUrl: 'header.component.html',
    styleUrls: ['header.style.css'],
    entryComponents: [UserMenu, LoginPageComponent]
})

export class HeaderComponent implements  AfterViewInit{

    @ViewChild('adHost', {read: ViewContainerRef}) adHost;
    @ViewChild('adLogin', {read: ViewContainerRef}) adLogin;

    widget: ComponentRef<any>;
    login: ComponentRef<any>;


    constructor(private _componentFactoryResolver: ComponentFactoryResolver,
                private auth:AuthService, private conf:ConfigurationService) { }

    ngAfterViewInit ( )
    {

            this.conf._get_config();
            let config = {'search_clear':'Some Value','items_title':'Categories'};
            this.conf.update_config('Landing_Page','selector',config);
            console.log();

            let UserMenu_componentFactory =
                this._componentFactoryResolver.resolveComponentFactory(UserMenu);
            this.widget = this.adHost.createComponent(UserMenu_componentFactory);

            let LoginPageComponent_componentFactory =
                this._componentFactoryResolver.resolveComponentFactory(LoginPageComponent);
            this.login = this.adLogin.createComponent(LoginPageComponent_componentFactory);



    }


}
