import {Component, OnInit} from '@angular/core';
import * as _ from 'lodash';
import {AjaxService} from './../../common/service/ajax.service';


interface IScenario {
    id: number;
    name: string;
    author: string;
    status: Object;
    permissions: Object;
    // {
    //     'selected': False,
    //     'disabled': False,
    // },

    // {
    //     'view': True,
    //     'edit': True,
    //     'delete': True
    // }
}

@Component({
    templateUrl: './scenarios-list.component.html',
    styleUrls: ['./scenarios-list.component.css']
})
export class ScenariosListComponent implements OnInit {
    private perPage: number = 3;
    private currentPage: number = null;
    private pagesNo: Array<number> = [];
    private all_sce: Array<any> = [];  // TODO Remake for IScenario
    private shown_sce: Array<any> = [];  // TODO Remake for IScenario

    constructor(private req: AjaxService) { }

    ngOnInit() {
        this.req.get({
            url_id: 'forecast/get_scenarios_list',
            data: {}
        }).subscribe((d) => {
            this.all_sce = [];
            if (d && _.isArray(d)) {
                for (let v of d) {
                    this.all_sce.push(v);
                }
            }
            this.pagesNo = _.range(1, _.ceil(this.all_sce.length/this.perPage)+1);
            this.showPage(1);
        });
    }
    showPage(page: number = 1) {
        if (page == this.currentPage) return false;

        let start = (page - 1) * this.perPage;
        if (start < this.all_sce.length) {
            this.shown_sce = _.slice(this.all_sce, start, start + this.perPage);
            this.currentPage = page;
        } else {
            if (page>1) {
                this.showPage(page - 1);
            } else {
                this.showPage(1);
            }
        }
    }
    clickView(id:number){
        console.log('View ' + id);
    }
    clickEdit(id:number){
        console.log('Edit ' + id);
    }
    clickDelete(id:number){
        console.log('Delete ' + id);
    }

}
