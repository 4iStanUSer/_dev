import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import {AjaxService} from "../../../common/service/ajax.service";
import { Location } from '@angular/common';

import { ScenarioModel } from "../scenario.model";


@Component({
    templateUrl: './new-scenario.component.html',
    styleUrls: ['../scenarios.component.css'],
})
export class NewScenarioComponent implements OnInit {
    save_status: boolean = false;
    scenario_id_param: number;
    scenario: ScenarioModel;
    new_scenario: any = {name: null, description: null};

    constructor(
        private router: Router,
        private req: AjaxService,
        private route: ActivatedRoute
    ) {}

    __getScenario() {
        if (this.scenario_id_param !== 0) {
            this.req.post({url_id: '/forecast/get_scenario_details', data: {'id': this.scenario_id_param}})
                .subscribe(
                    (data) => {
                        this.scenario = new ScenarioModel(
                            data.id, data.author, data.criteria, data.name, data.description,
                            data.favorite, data.modify_date, data.shared, data.status, data.scenario_permission
                        );
                    }
                );
        }
        if (this.scenario === null) {
            // TODO Add 404
            this.router.navigate(["../../scenarios-list"], { relativeTo: this.route });
        }
    }

    __checkPermission() {
        if (this.scenario !== undefined && this.scenario.checkPermission('edit') === false) {
            // TODO Add 403
            this.router.navigate(["../../scenarios-list"], { relativeTo: this.route });
        }
    }

    __getCriteria() {
        return 'USA-Main-Weapon'
    }

    __createScenario() {
        this.req.post({
            url_id: '/forecast/create_scenario',
            data: {
                'name': this.new_scenario.name,
                'description': this.new_scenario.description,
                'status': 'New',
                'shared': 'No',
                'criteria': this.__getCriteria()
            },
        }).subscribe((data) => {
                if(!isNaN(data['id'])) {
                    this.save_status = true;
                } else {
                    // TODO add error message
                }
            }
        );
    }

    __editScenario() {
        this.req.post({
            url_id: '/forecast/edit_scenario',
            data: [{id: this.scenario_id_param, 'modify':[
                {parameter:'name', value: this.scenario.name},
                {parameter:'description', value: this.scenario.description},
                ]
            }],
        }).subscribe((data) => {
                if(data.error !== true) {
                    this.save_status = true;
                } else {
                    // TODO add error message
                }
            }
        );
    }

    __saveScenario() {
        if (this.scenario_id_param === 0) {
            this.__createScenario();
        } else {
            this.__editScenario();
        }
    }

    ngOnInit(): void {
        this.route.params.subscribe(params => {
            if (params['id']) {
                if (isNaN(params['id'])){
                    this.router.navigate(["../../scenarios-list"], { relativeTo: this.route });
                } else {
                    this.scenario_id_param = parseInt(params['id']);
                }
            } else {
                this.scenario_id_param = 0;
            }
        });
        // Get scenario
        this.__getScenario();

        // Check permissions
        this.__checkPermission();
    }

    onClear(param: string) {
        this.new_scenario[param] = null;
        this.scenario[param] = null;
    }

    onCancel() {
        if (this.scenario_id_param !== 0) {
            this.router.navigate(["../../scenarios-list"], { relativeTo: this.route });
        } else {
            this.router.navigate(["../scenarios-list"], { relativeTo: this.route });
        }
    }

    onSaveGo(event: any) {
        event.preventDefault();
        this.save_status = false;
        this.__saveScenario();
        setTimeout(() => {
            // TODO Add run simulator
            if (this.scenario_id_param !== 0) {
                this.router.navigate(["../../../simulator"], { relativeTo: this.route });
            } else {
                this.router.navigate(["../../simulator"], { relativeTo: this.route });
            }
        }, 300);
    }

    onSaveClose(event: any) {
        event.preventDefault();
        this.save_status = false;
        this.__saveScenario();
        setTimeout(() => {
            if (this.save_status) {
                this.onCancel();
            }
        }, 300);
    }
}
