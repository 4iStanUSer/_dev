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
            .post({
                'url_id': 'landing',
                'data': {}
}
            )
            .subscribe((tools: Object) => {
                console.log('LandingPageComponent->ngOnInit', tools);
                this.tools = tools;
            });
    }

    onToolChange(toolKey: string) {
        this.currProject = null;
    }

    goToTool(toolKey: string, projectId: string) {
        this.req.post({ // TODO Make post query
            'url_id': 'set_tool_selection',
            'data': {
                'tool_id': toolKey,
                'project_id': projectId
            }
        }).subscribe((tools) => {
            console.log('LandingPageComponent->goToTool', tools);
            this.router.navigate([toolKey]);
        });
    }

}
