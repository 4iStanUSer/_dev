import {Component, OnInit} from '@angular/core';
import {
    MenuWidgetDataInput
} from "./menu-widget/menu-widget.component";
import {AjaxService} from "../common/service/ajax.service";

@Component({
    templateUrl: './forecast.component.html',
    styleUrls: ['./forecast.component.css']
})
export class ForecastComponent implements OnInit {

    private topMenuData: MenuWidgetDataInput = null;

    constructor(private req: AjaxService) {
    }

    ngOnInit() {
        this.req.get({
            url: 'get-menu', // TODO Implement on server
            data: {}
        }).subscribe(
            (d) => {
                // this.topMenuData = d['menu'];
            }
        );
        this.topMenuData = [
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
    }

}
