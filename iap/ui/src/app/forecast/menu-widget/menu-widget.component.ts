import {
    Component,
    Input,
    OnInit,
    OnChanges,
    SimpleChanges
} from '@angular/core';

import {Router} from '@angular/router';

class MenuWidgetDataItemInput {
    key: string = null;
    name: string = null;
    disabled: boolean = false;
}
export type MenuWidgetDataInput = Array<MenuWidgetDataItemInput>;

class MenuWidgetDataItem extends MenuWidgetDataItemInput {
    path: string = null;
}
export type MenuWidgetData = Array<MenuWidgetDataItem>;

@Component({
    selector: 'menu-widget',
    templateUrl: './menu-widget.component.html',
    styleUrls: ['./menu-widget.component.css']
})
export class MenuWidgetComponent implements OnInit, OnChanges {

    private links: MenuWidgetData = [
        {
            key: 'home',
            name: 'Home',
            disabled: false,
            path: '/landing'
        },
        {
            key: 'dashboard',
            name: 'Dashboard',
            disabled: false,
            path: '/forecast/dashboard'
        },
        {
            key: 'comparison',
            name: 'Comparison',
            disabled: false,
            path: null
        },
        {
            key: 'scenarios',
            name: 'Scenarios',
            disabled: false,
            path: '/forecast/scenarios'
        },
        {
            key: 'simulator',
            name: 'Simulator',
            disabled: false,
            path: '/forecast/simulator'
        },
        // {
        //     key: 'help',
        //     name: 'Help',
        //     disabled: false,
        //     path: null
        // }
    ];

    private linksMap: {
        [linkKey: string]: number
    } = {};

    @Input() data: MenuWidgetDataInput = [];

    constructor(private router: Router) {
        if (this.links && this.links.length) {
            this.linksMap = {};
            let l = this.links.length;
            for (let i = 0; i < l; i++) {
                this.linksMap[this.links[i].key] = i;
            }
        }
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['data'] && ch['data']['currentValue']) {
            console.log(ch['data']['currentValue']);
            let l = ch['data']['currentValue'].length;
            for (let i = 0; i < l; i++) {
                let item = ch['data']['currentValue'][i];
                try {
                    let linkIndex = this.linksMap[item.key];
                    this.links[linkIndex].name = item.name;
                    this.links[linkIndex].disabled = item.disabled;
                } catch (e) {
                    console.error(e);
                }
            }
        }
    }

    onClickLink(link: MenuWidgetDataItem, e: MouseEvent) {
        e.preventDefault();
        if (link && link['route'] && link['route'].length) {
            this.router.navigate([link['route']]);
        }
    }
}
