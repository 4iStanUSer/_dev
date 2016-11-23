import {Component, OnInit} from '@angular/core';
import {
    MenuWidgetDataInput
} from "./menu-widget/menu-widget.component";
import {AjaxService} from "../common/service/ajax.service";
import {
    LanguageSelectorInput,
    LanguageSelectorOutput
} from "./language-selector/language-selector.component";

@Component({
    templateUrl: './forecast.component.html',
    styleUrls: ['./forecast.component.css']
})
export class ForecastComponent implements OnInit {

    private topMenuData: MenuWidgetDataInput = null;

    private langsData: LanguageSelectorInput = null;

    constructor(private req: AjaxService) {
    }

    ngOnInit() {
        this.req.get({
            url_id: 'get_languages', // TODO Change url
            data: {}
        }).subscribe(
            (d) => {
                this.langsData = <LanguageSelectorInput>d;
            }
        );

        this.req.get({
            url_id: 'forecast/get_top_menu', // TODO Change url
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

}
