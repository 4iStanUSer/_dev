import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AjaxService} from "../common/service/ajax.service";

import {TOP_MENU_CONTENT} from "./top-menu.content"
import {Client, User, MenuItem, LanguageItem} from "../app.model"

import {AuthService} from "../common/service/auth.service";

@Component({
    templateUrl: './forecast.component.html',
    styleUrls: ['./forecast.component.css']
})
export class ForecastComponent implements OnInit {

    private menuItems: MenuItem[] = TOP_MENU_CONTENT;
    private user: User;
    private client: Client;
    private langsList: LanguageItem[] = [];
    private logoutLabel: string = 'Log Out';

    constructor(
        private req: AjaxService,
        private auth: AuthService,
        public router: Router
    ) {}

    ngOnInit() {
        this.req.post({
            url_id: 'get_page_configuration',
            data: {'page': 'common'}
        }).subscribe(
            (d) => {
                this.proceedPageConfig(d);
            }
        );
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

    private proceedPageConfig(inputs: Object): void {
        if (inputs['logout***label']) {
            this.logoutLabel = inputs['logout_label'];
        }
        let l = this.menuItems.length;
        for (let i = 0; i < l; i++) {
            let itemKey = this.menuItems[i].key;
            if (inputs['top_menu***' + itemKey]) {
                this.menuItems[i].name = inputs['top_menu***' + itemKey]
            }
        }
    }

    languageChanged(newLangId: string) {
        this.req.post({
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
