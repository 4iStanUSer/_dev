import { Component } from '@angular/core';
// import { Router } from '@angular/router';
// import * as _ from 'lodash';

// TODO Update 3-rd party including - https://github.com/angular/angular-cli#global-styles

@Component({
    selector: 'app-root',
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css']

})
export class AppComponent {

    constructor() { }


    // constructor(private _router: Router) { }
    // /**
    //  * Handler for menu item click
    //  * @param item
    //  * @returns
    //  */
    // menuClicked(item) {
    //     if (!item || item.disabled) return false;
    //
    //     if (_.size(item.app_link) > 0) {
    //         this._router.navigate([item.app_link]);
    //     } else if (item.func && _.isFunction(item.func)) {
    //         item.func(item);
    //     } else if (_.size(item.href) > 0) {
    //         console.log(item.href);
    //     } else {
    //         console.warn('Have no operation for menu click handler!');
    //     }
    // }
    //
    //
    // menuHandler(item) {
    //     console.log("Clicked " + item.name);
    // }
    // menu: Array<any> = [
    //     {
    //         "name": "Item 1",
    //         "disabled": false,
    //         "func": this.menuHandler,
    //         "children": [
    //             {
    //                 "name": "Index",
    //                 "disabled": false,
    //                 "app_link": "forecast"
    //             },
    //             {
    //                 "name": "Scenarios",
    //                 "disabled": false,
    //                 "app_link": "forecast/scenarios"
    //             },
    //             {
    //                 "name": "Edit",
    //                 "disabled": false,
    //                 "app_link": "forecast/edit"
    //             }
    //         ]
    //     },
    //     {
    //         "name": "Item 2",
    //         "href": "/",
    //         "disabled": false,
    //         //"func": this.menuHandler,
    //         "children": [
    //             {
    //                 "name": "Item 21", "disabled": false, "children": [],
    //                 "func": this.menuHandler,
    //             },
    //             {
    //                 "name": "Item 22", "disabled": true, "children": [],
    //                 "func": this.menuHandler,
    //             }
    //         ]
    //     },
    //     {
    //         "name": "Item 3", "disabled": false, "children": [],
    //         "func": this.menuHandler,
    //     }
    // ];
}
