import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AjaxService} from "../../common/service/ajax.service";

@Component({
  selector: 'tool-selector',
  templateUrl: './tool-selector.component.html',
  styleUrls: ['./tool-selector.component.css']
})
export class ToolSelectorComponent implements OnInit {

    private mock_projects: Object = {
  "forecast": [
    {
      "id": "ft-module-name1",
      "short_name": "FT-Module Name1",
      "full_name": "FT-Module Name1",
      "description": "FT-Module Description1",
      "icon": "ft-module-icon1.svg"
    },
    {
      "id": "ft-module-name2",
      "short_name": "FT-Module Name2",
      "full_name": "FT-Module Name2",
      "description": "FT-Module Description2",
      "icon": "ft-module-icon2.svg"
    }
  ],
  "pp": [
    {
      "id": "pp-module-name1",
      "short_name": "PP-Module Name1",
      "full_name": "PP-Module Name1",
      "description": "PP-Module Description1",
      "icon": "pp-module-icon1.svg"
    },
    {
      "id": "pp-module-name2",
      "short_name": "PP-Module Name2",
      "full_name": "PP-Module Name2",
      "description": "PP-Module Description2",
      "icon": "pp-module-icon2.svg"
    }
  ],
  "mm": [
    {
      "id": "mm-module-name1",
      "short_name": "MM-Module Name1",
      "full_name": "MM-Module Name1",
      "description": "MM-Module Description1",
      "icon": "mm-module-icon1.svg"
    },
    {
      "id": "mm-module-name2",
      "short_name": "MM-Module Name2",
      "full_name": "MM-Module Name2",
      "description": "MM-Module Description2",
      "icon": "mm-module-icon2.svg"
    }
  ]
};
    private projects: Object = null;
    private mock_lp_config: Object = {
        "forecast_id": "forecast",
        "forecast_name": "Forecasting",
        "forecast_description": "Forecasting Forecasting",
        "forecast_image": "forecast.jpg",
        "pp_id": "pp",
        "pp_name": "Price and promo",
        "pp_description": "Price and promo Price and promo",
        "pp_image": "pp.jpg",
        "mm_id": "mm",
        "mm_name": "Market mix",
        "mm_description": "Market mix Market mix",
        "mm_image": "mm.jpg"
    };
    private lp_config: Object = null;
    private mock_user_config: Object = {
        "user_info": {
            "user_name": "Nicolas",
            "company_name": "CompanyASD",
            "company_logo": "logo.jpg"
        }
    };
    private user_config: Object = null;

    /*
    private tools: Object = null;
    private mock_tools: Object = {
        "forecast": {
            "name": "Forecasting",
            "projects": [
                {
                    "id": "ft-module-name1",
                    "name": "FT-Module Name1"
                },
                {
                    "id": "ft-module-name2",
                    "name": "FT-Module Name2"
                }
            ]
        },
        "pp": {
            "name": "Price and promo",
            "projects": [
                {
                    "id": "pp-module-name1",
                    "name": "PP-Module Name1"
                },
                {
                    "id": "pp-module-name2",
                    "name": "PP-Module Name2"
                }
            ]
        },
        "mm": {
            "name": "Market mix",
            "projects": [
                {
                    "id": "mm-module-name1",
                    "name": "MM-Module Name1"
                },
                {
                    "id": "mm-module-name2",
                    "name": "MM-Module Name2"
                }
            ]
        }
    };
    */


    constructor(private router: Router, private req: AjaxService) {

    }

    ngOnInit() {
        // TODO replace mock objects with server data
        this.user_config = this.mock_user_config;
        this.projects = this.mock_projects;
        this.lp_config = this.mock_lp_config;



        /*
        this.tools = this.mock_tools;
        console.log('LandingPageComponent->ngOnInit', this.tools);
        this.req
            .get({
                'url_id': 'landing',
                'data': {}
            })
            .subscribe((tools: Object) => {
                console.log('LandingPageComponent->ngOnInit', tools);
                this.tools = tools;
            });*/
    }

    goToTool(toolKey: string, projectId: string) {
        this.req.get({ // TODO Make post query
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

    showTool(user_config: Object, projects: Object, tool_id: string ): boolean {
        //user is not authorized
        if (user_config === null && projects === null ){
            return true;
        }
        // user is authorized and user has projects available for the passed tool_id
        else if (user_config !== null && tool_id in projects) {
            return true;
        }
        else {
            return false;
        }
    }

}
