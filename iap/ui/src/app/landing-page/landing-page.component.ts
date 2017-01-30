import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

import {AjaxService} from "../common/service/ajax.service";
import {AuthService} from "../common/service/auth.service";
import {LanguageItem, User, Client} from "../app.model";



@Component({
    templateUrl: './landing-page.component.html',
    styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {

    private user: User;
    private client: Client;
    private langsList: LanguageItem[] = [];

    constructor(private router: Router, private req: AjaxService, private auth: AuthService) {
    }

    ngOnInit() {

        this.req.post({
            url_id: 'get_header_data',
            data: {}
        }).subscribe(
            (d) => {
                this.proceedHeaderInputs(d);
            }
        );

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
        this.req.get({
            url_id: 'set_language',
            data: { 'lang': newLangId }
        }).subscribe(
            (d) => {
                console.log('lang_changed');
            }
        );
    }

    onClickLogout() {
        this.auth.logout()
            .subscribe(
                () => {
                    this.router.navigate(['/']);
                },
                (e) => {
                    console.log(e);
                },
                () => {
                    console.log('Complete!');
                }
            );
    }

}
