import {Component, AfterViewInit, ComponentFactoryResolver, ViewChild, ViewContainerRef, ComponentRef} from '@angular/core';
import { TestComponent } from '../notification/test.components';
import { LoginPageComponent } from '../login-page/page/login-page.component'
import { MenuWidgetComponent } from '../../forecast/menu-widget/menu-widget.component';
import { AuthHttp } from 'angular2-jwt';
import { Http } from '@angular/http';
import { AuthService } from '../../common/login-page/auth.service';

@Component({
    selector: 'new_header',
    templateUrl: 'header.component.html',
    styleUrls: ['header.style.css'],
    entryComponents: [TestComponent, LoginPageComponent, MenuWidgetComponent]
})

export class HeaderComponent implements  AfterViewInit{

    @ViewChild('adHost', {read: ViewContainerRef}) adHost;
    @ViewChild('adLogin', {read: ViewContainerRef}) adLogin;

    widget: ComponentRef<any>;
    login: ComponentRef<any>;


    constructor(private _componentFactoryResolver: ComponentFactoryResolver,
                private auth:AuthService, private auth_http: AuthHttp, private http: Http) { }

    ngAfterViewInit ( )
    {


        if (this.auth.isLoggedIn()){
            /*
            If user authorised render this component
             */
            let componentFactory =
                this._componentFactoryResolver.resolveComponentFactory(LoginPageComponent);
            this.widget = this.adHost.createComponent(componentFactory);



        }
        else{

            /*
            If user unauthorised render this component
             */
            this.http.post('/get_header_data', {}).subscribe((d) => {console.log(d)});

            let _componentFactory =
                this._componentFactoryResolver.resolveComponentFactory(LoginPageComponent);
            this.login = this.adLogin.createComponent(_componentFactory);


            let componentFactory =
                this._componentFactoryResolver.resolveComponentFactory(TestComponent);


            this.widget = this.adHost.createComponent(componentFactory);
        }

    }


}
