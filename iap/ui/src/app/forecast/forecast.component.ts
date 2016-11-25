import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {
    MenuWidgetDataInput
} from "./menu-widget/menu-widget.component";
import {AjaxService} from "../common/service/ajax.service";
import {
    LanguageSelectorInput,
    LanguageSelectorOutput
} from "./language-selector/language-selector.component";
import {AuthService} from "../common/service/auth.service";

@Component({
    templateUrl: './forecast.component.html',
    styleUrls: ['./forecast.component.css']
})
export class ForecastComponent implements OnInit {

    private topMenuData: MenuWidgetDataInput = null;

    private langsData: LanguageSelectorInput = null;

    constructor(
        private req: AjaxService,
        private auth: AuthService,
        public router: Router
    ) {
    }

    ngOnInit() {
        this.req.get({
            url_id: 'get_languages',
            data: {}
        }).subscribe(
            (d) => {
                this.langsData = <LanguageSelectorInput>d;
            }
        );

        this.req.get({
            url_id: 'forecast/get_top_menu',
            data: {}
        }).subscribe(
            (d) => {
                this.topMenuData = <MenuWidgetDataInput>d;
            }
        );
    }

    languageChanged(changes: LanguageSelectorOutput) {
        console.log(changes);
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
