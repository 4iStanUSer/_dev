import {Injectable} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Injectable()
export class BreadcrumbsService {

    static pathKey: string = 'breadcrumbs';

    private routesKeys: {[componentKey: string]: string} = {
        'forecast': 'Home',
        'dashboard': 'Dashboard',
        'general': 'General'
    };

    constructor(private route: ActivatedRoute) {
    }

    getFullPath() {
        return this.getPathRecursively(this.route);
    }

    private getPathRecursively(root: ActivatedRoute) {
        let path = [];

        console.log(root);
        console.log(root.component); //.component[BreadcrumbsService.pathKey]
        console.log(root.component[BreadcrumbsService.pathKey]);

        if (root.firstChild) {
            this.getPathRecursively(root.firstChild);
        }

    }

}
