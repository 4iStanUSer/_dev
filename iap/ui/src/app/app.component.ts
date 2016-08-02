import { Component } from '@angular/core';
import { ROUTER_DIRECTIVES, Router } from '@angular/router';
import * as _ from 'lodash';
import { MenuWidgetComponent } from './common/cmp/menu-widget/';
//import { DatepickerComponent } from './components/datepicker.component';
import { AjaxService, Loading } from './common/service/request.service';
import { ComponentFactoryService } from './common/service/component-factory.service';
import { MachineGunnerService } from './common/service/machine-gunner.service';
import { IndexPageService } from "./forecast/service/index-page.service";



@Component({
    moduleId: module.id,
    selector: 'app-root',
    directives: [ROUTER_DIRECTIVES, MenuWidgetComponent],
    providers: [AjaxService, Loading, MachineGunnerService, ComponentFactoryService], //IndexPageService
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css']
})
export class AppComponent {
    constructor(private _router: Router) { }

    /**
     * Handler for menu item click
     * @param item
     * @returns
     */
    menuClicked(item) {
        if (!item || item.disabled) return false;

        if (_.size(item.app_link) > 0) {
            this._router.navigate([item.app_link]);
        } else if (item.func && _.isFunction(item.func)) {
            item.func(item);
        } else if (_.size(item.href) > 0) {
            console.log(item.href);
        } else {
            console.warn('Have no operation for menu click handler!');
        }
    }


    menuHandler(item) {
        console.log("Clicked " + item.name);
    }
    menu: Array<any> = [
        {
            "name": "Item 1",
            "disabled": false,
            "func": this.menuHandler,
            "children": [
                {
                    "name": "Index",
                    "disabled": false,
                    "app_link": "forecast"
                },
                {
                    "name": "Tree",
                    "disabled": false,
                    "app_link": "forecast/edit"
                }
            ]
        },
        {
            "name": "Item 2",
            "href": "/",
            "disabled": false,
            //"func": this.menuHandler,
            "children": [
                {
                    "name": "Item 21", "disabled": false, "children": [],
                    "func": this.menuHandler,
                },
                {
                    "name": "Item 22", "disabled": true, "children": [],
                    "func": this.menuHandler,
                }
            ]
        },
        {
            "name": "Item 3", "disabled": false, "children": [],
            "func": this.menuHandler,
        }
    ];
}
