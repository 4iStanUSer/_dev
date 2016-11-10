import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

import {AjaxService} from "./../../service/ajax.service";


interface ToolsAndProjectsInput {
    [tool_name: string]: {
        name: string,
        projects: Array<{
            id: string,
            name: string
        }>
    };
}

@Component({
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
        this.req
            .get({
                'url': 'landing',
                'data': {}
            })
            .subscribe((tools: Object) => {
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
            this.router.navigate([toolKey]);
        });
    }

}
