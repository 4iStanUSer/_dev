import {Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';


@Component({
    templateUrl: './simulator-page.component.html',
    styleUrls: ['./simulator-page.component.css']
})
export class SimulatorPageComponent implements OnInit {
    constructor(
        private router: Router
    ) {}

    ngOnInit() {
    }

    isRouteActive(route: any) {
        // this.router.navigate(route);
        console.log(this.router);
    }
}
