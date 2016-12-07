import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AjaxService} from "../../common/service/ajax.service";

import {Tool, Project} from "../../app.model"

@Component({
  selector: 'tool-selector',
  templateUrl: './tool-selector.component.html',
  styleUrls: ['./tool-selector.component.css']
})
export class ToolSelectorComponent implements OnInit {

    private forecastingTool: Tool = new Tool();
    private pptTool: Tool = new Tool();
    private mmTool: Tool = new Tool();

    constructor(private router: Router, private req: AjaxService) {}

    ngOnInit() {
        this.forecastingTool.id = "forecast";
        this.pptTool.id = "ppt";
        this.mmTool.id = "mm";
        this.req
            .get({
                'url_id': 'get_tools_with_projects',
                'data': {}
            })
            .subscribe((d) => {
                this.processInputs(d);
            });
    }

    processInputs(inputs: Object) {
        let tools_data = inputs['tools'];
        if (tools_data) {
            console.log('tools in inputs');
            let l = tools_data.length;
            for (let i = 0; i < l; i++) {
                let row = tools_data[i];
                console.log('row', row['id'], row['name']);
                if (row['id'] === this.forecastingTool.id) {
                    this.forecastingTool.init(row);
                }
                if (row['id'] === this.pptTool.id) {
                    this.pptTool.init(row);
                }
                if (row['id'] === this.mmTool.id) {
                    this.mmTool.init(row);
                }
            }
        }
        let projects_data = inputs['projects'];
        if (projects_data) {
            let l = projects_data.length;
            for (let i = 0; i < l; i++) {
                let row = projects_data[i];
                let p = new Project();
                p.init(row);
                if (row['tool_id'] === this.forecastingTool.id) {
                    this.forecastingTool.projects.push(p);
                }
                if (row['tool_id'] === this.pptTool.id) {
                    this.pptTool.projects.push(p);
                }
                if (row['tool_id'] === this.mmTool.id) {
                    this.mmTool.projects.push(p);
                }
            }
        }
    }

    goToTool(toolId: string, projectId: string) {
        this.req.get({ // TODO Make post query
            'url_id': 'select_project',
            'data': {
                'tool_id': toolId,
                'project_id': projectId
            }
        }).subscribe((tools) => {
            this.router.navigate([toolId]);
        });
    }
}
