import {
    Component,
    Input
} from '@angular/core';

import {Router} from '@angular/router';
import { MenuItem } from "../../app.model"

@Component({
    selector: 'menu-widget',
    templateUrl: './menu-widget.component.html',
    styleUrls: ['./menu-widget.component.css']
})
export class MenuWidgetComponent {

    @Input() menu: MenuItem[] = [];

    constructor(private router: Router) {}

    onClickLink(link: MenuItem, e: MouseEvent) {
        e.preventDefault();
        if (link && link['route'] && link['route'].length) {
            this.router.navigate([link['route']]);
        }
    }
}
