import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AjaxService } from "../../../common/service/ajax.service";

import { ScenarioModel } from "../scenario.model";


@Component({
    templateUrl: './new-scenario.component.html',
    styleUrls: ['../scenarios.component.css'],
})
export class NewScenarioComponent implements OnInit {
    save_status: boolean = false;
    scenario_id_param: number;
    scenario: ScenarioModel;
    new_scenario: any = {name: '', description: ''};
    form_status: any = {
        valid: false,
        messages: {
            name: 'Field is required',
            description: 'Field is required'
        }
    };

    predifined_drivers:any = [
        {
            label: 'Climate',
            name: 'climate',
            options: [
                {name: '1', value: '1a'},
                {name: '2', value: '2a'},
                {name: '3', value: '3a'},
            ]
        },
        {
            label: 'Macroeconomic',
            name: 'macroeconomic',
            options: [
                {name: '3', value: '3a'},
                {name: '4', value: '4a'},
                {name: '5', value: '5a'},
            ]
        }
    ];

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
                        this.new_scenario.name = data.name;
                        this.new_scenario.description = data.description;
                        this.scenario = data;
                        this.form_status.valid = true;
                        this.form_status.messages = {};
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
                'status': 'Draft',
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
                {parameter:'name', value: this.new_scenario.name},
                {parameter:'description', value: this.new_scenario.description},
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

    onChangeForm(event:any) {
        this.new_scenario[event.target.name] = event.target.value;
        this.__checkFormValid(event.target.name, event.target.value);
    }

    __checkFormValid(field, value) {
        if (!value) {
            this.form_status.messages[field] = 'Field is required';
        } else {
            delete this.form_status.messages[field];
        }

        if (Object.keys(this.form_status.messages).length > 0) {
            this.form_status.valid = false;
        } else {
            this.form_status.valid = true;
        }
        console.log(this.form_status.messages, this.form_status.valid);
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


        for (let i in this.predifined_drivers) {
            console.log(this.predifined_drivers[i]);
            this.new_scenario[this.predifined_drivers[i].name] = '';
            this.__checkFormValid(this.predifined_drivers[i].name, false);
        }
    }

    onClear(param: string) {
        this.new_scenario[param] = '';
        this.__checkFormValid(param, false);
    }

    onCancel() {
        if (this.scenario_id_param !== 0) {
            this.router.navigate(["../../scenarios-list"], { relativeTo: this.route });
        } else {
            this.router.navigate(["../scenarios-list"], { relativeTo: this.route });
        }
    }

    onSaveGo(event: any) {
        if (this.form_status.valid) {
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
    }

    onSaveClose(event: any) {
        if (this.form_status.valid) {
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

    onSaveNew(event: any) {
        if (this.form_status.valid) {
            event.preventDefault();
            this.save_status = false;

            //Create new scenario
            this.new_scenario.name = 'New '.concat(new Date().getTime().toString(), ' ', this.scenario.name);
            this.new_scenario.description = this.scenario.description;
            this.__createScenario();
            setTimeout(() => {
                if (this.save_status) {
                    this.onCancel();
                }
            }, 300);
        }
    }
}
