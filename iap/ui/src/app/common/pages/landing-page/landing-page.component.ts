import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

import {AjaxService} from "../../service/ajax.service";

@Component({
    selector: 'landing-page',
    templateUrl: './landing-page.component.html',
    styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {

    private tools: Object = null;
    private currTool: string = null;
    private currProject: Object = null;

    constructor(private router: Router, private req: AjaxService) {
    }

    ngOnInit() {
        // let a = {
        //     'forecast': {
        //         name: 'Forecasting Tool',
        //         projects: [
        //             {id: 'JJOralCare', name: 'FT JJ Oral Care'},
        //             {id: 'JJLean', name: 'FT JJ Lean Forecasting'}
        //         ]
        //     },
        // };
        this.req
            .get({
                'url': 'landing',
                'data': {}
            })
            .subscribe((tools) => {
                this.tools = tools;
            });
    }

    onToolChange(toolKey: string) {
        this.currProject = null;
    }

    goToTool(toolKey: string, projectId: string) {
        this.req.get({
            'url': 'set_tool_selection',
            'data': {
                'tool_id': toolKey,
                'project_id': projectId
            }
        }).subscribe((tools) => {
            //this.router.navigate([toolKey]);
        });

        // TODO - Remove this when request will be successful(VL)
        this.router.navigate([toolKey]);
    }

}
