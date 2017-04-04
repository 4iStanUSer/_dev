import {Component, OnInit} from '@angular/core';
import {LanguageItem, User, Client} from "../app.model";
import { AuthHttp} from 'angular2-jwt';
import { Http } from '@angular/http';
import { AuthService } from '../common/login-page/auth.service';



@Component({
    templateUrl: './landing-page.component.html',
    styleUrls: ['./landing-page.component.css']
})
export class  LandingPageComponent implements OnInit {

    private user: User;
    private client: Client;
    private langsList: LanguageItem[] = [];

    constructor(private auth_http: AuthHttp, private http: Http, private auth: AuthService) {
    }

    ngOnInit() {

        if(this.auth.isLoggedIn()) {

            this.auth_http.post('get_header_data', {}).subscribe(
                (d) => {
                    this.proceedHeaderInputs(d);
                }
            );
        }
        else{

            this.http.post('get_header_data', {}).subscribe(
                (d) => {
                    this.proceedHeaderInputs(d);
                }
            );
        }

    }
    private proceedHeaderInputs(inputs: Object): void {
        if (inputs['client']) {
            this.client = new Client();
            this.client.init(inputs['client']);
        }
        if (inputs['user']) {
            this.user = new User();
            this.user.init(inputs['user']);
        }
        if (inputs['languages']) {
            let l = inputs['languages'].length;
            for (let i = 0; i < l; i++) {
                let row = inputs['languages'][i];
                this.langsList.push(<LanguageItem>row);
            }
        }
    }

    languageChanged(newLangId: string) {

        if(this.auth.isLoggedIn()) {

            this.auth_http.post('set_language', {'data': { 'lang': newLangId }}).subscribe(
            (d) => {
                console.log('lang_changed');
                 }
            );
        }
        else{

            this.http.post('set_language', {'data': { 'lang': newLangId }}).subscribe(
            (d) => {
                console.log('lang_changed');
                }
            );
        }
    }

}


