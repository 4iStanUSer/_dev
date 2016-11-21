import {Component, OnInit} from '@angular/core';
import {
    MenuWidgetDataInput
} from "./menu-widget/menu-widget.component";
import {AjaxService} from "../common/service/ajax.service";
import {
    LanguageSelectorInput,
    LanguageSelectorOutput
} from "./language-selector/language-selector.component";

const langsDataTEMP = [
    {
        id: 'en',
        name: 'English',
        selected: true
    },
    {
        id: 'ru',
        name: 'Russian',
        selected: false
    },
    {
        id: 'sp',
        name: 'Spain',
        selected: false
    },
];
const topMenuDataTEMP = [
    {
        key: 'comparison',
        name: 'Comparison',
        disabled: true
    },
    {
        key: 'scenarios',
        name: 'Scenarios',
        disabled: false
    },
    {
        key: 'simulator',
        name: 'Simulator',
        disabled: false
    },
];

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
            url: 'get-languages', // TODO Implement on server
            data: {}
        }).subscribe(
            (d) => {
                // this.langsData = d['langs'];
            }
        );

        this.req.get({
            url: 'get-menu', // TODO Implement on server
            data: {}
        }).subscribe(
            (d) => {
                // this.topMenuData = d['menu'];
            }
        );

        // TEMP below
        this.langsData = langsDataTEMP;
        this.topMenuData = topMenuDataTEMP;
    }

    languageChanged(changes: LanguageSelectorOutput) {
        console.log(changes);
    }

}
