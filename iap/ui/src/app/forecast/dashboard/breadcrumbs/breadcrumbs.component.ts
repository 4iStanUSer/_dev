import {Component, OnInit} from '@angular/core';
import {BreadcrumbsService} from "./breadcrumbs.service";

@Component({
    selector: 'breadcrumbs',
    templateUrl: './breadcrumbs.component.html',
    styleUrls: ['./breadcrumbs.component.css']
})
export class BreadcrumbsComponent implements OnInit {

    private path: Array<Object> = [];

    constructor(private service: BreadcrumbsService) {
    }

    ngOnInit() {
        // console.log();
        this.service.getFullPath()
    }

}
