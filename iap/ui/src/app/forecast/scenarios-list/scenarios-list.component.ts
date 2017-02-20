import { Component, OnInit, DoCheck } from '@angular/core';
import {AjaxService} from "../../common/service/ajax.service";

import { ScenariosListComponentService } from './scenarios-list.service';
// import lowerCase = require("lower-case");
const moment = require('moment/moment');
const DATEFORMAT = 'MM.DD.YY';


@Component({
    templateUrl: './scenarios-list.component.html',
    styleUrls: ['./scenarios-list.component.css'],
    providers: [ScenariosListComponentService]
})
export class ScenariosListComponent implements OnInit {
    scenariosList: any[];
    user_permissions: any[]; // remove
    userPermissionsData: any[];
    selectedScenarios: any[];
    favoriteList: any;
    selectElement: any;
    selectScenario: any;
    search: string;

    //Permissions
    userPermissions: any = {
        create: false,
        finalize: false,
        share: false,
        copy: false,
        delete: false
    };

    constructor(private req: AjaxService) { }

    // Parse date 2017-02-10 14:00:13.990018 to DATEFORMAT
    dateParse(dateString: string) {
        return moment(Date.parse(dateString)).format(DATEFORMAT);
    }

    __getKey(key:string, obj:any, def:any=false) {
        let value = def;
        if (obj !== null && typeof obj === 'object') {
            if (obj.hasOwnProperty(key)) {
                value = obj[key];
            }
        }
        return value;
    }

    in_array(what, where) {
        for(var i=0; i<where.length; i++)
            if(what === where[i])
                return true;
        return false;
    }

    ngOnInit(): void {
        this.getScenariosList();
        this.__loadUserPermissionsData();
        this.selectedScenarios = [];
    }

    ngDoCheck(): void {
        // Check permissions
        this.__initUserPermissions();
    }

    // Get scenarios list from server
    getScenariosList() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.scenariosList = data.data;
        });
        console.log('---getScenariosList');
    }
    // ---------------------------------  Build filter  ----------------------------------//
    getFavoriteListLength() {
        try {
            return this.favoriteList.length;
        } catch(e) {
            return 0;
        }
    }
    getFavoriteList() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            this.favoriteList = [];
            for (let i = 0; i < this.scenariosList.length; i++) {
                if (this.scenariosList[i].favorite === true) {
                    this.favoriteList.push(this.scenariosList[i].id);
                }
            }
        }
    }
    getSharedCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const sharedList = this.scenariosList.filter((item) => {
                return item.shared.toLowerCase() === 'yes';
            });
            return sharedList.length;
        } else {
            return 0;
        }
    }
    getLocalCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const localList = this.scenariosList.filter((item) => {
                return item.shared.toLowerCase() === 'no';
            });
            return localList.length;
        } else {
            return 0;
        }
    }
    getFinalStatusCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const finalStatusList = this.scenariosList.filter((item) => {
                return item.status.toLowerCase() == 'final'
            });
            return finalStatusList.length;
        } else {
            return 0;
        }
    }
    getNewStatusCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const finalStatusList = this.scenariosList.filter((item) => {
                return item.status.toLowerCase() == 'new'
            });
            return finalStatusList.length;
        } else {
            return 0;
        }
    }
    getDraftsStatusCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const draftsStatusList = this.scenariosList.filter((item) => {
                return item.status.toLowerCase() == 'draft'
            });
            return draftsStatusList.length;
        } else {
            return 0;
        }
    }
    getAuthorsList() {
        let authorsList = [];
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            for (const i in this.scenariosList) {
                authorsList.push(this.scenariosList[i].author);
            }
            return authorsList.filter((el, i, arr) => arr.indexOf(el) === i);
        }
    }
    // ---------------------------------  Build filter  ----------------------------------//

    // -------------------------------  Check permissions  -------------------------------//
    // Get user permissions from server
    __loadUserPermissionsData() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.userPermissionsData = data.user_permission;
        });
    }

    __initUserPermissions() {
        this.__clearUserPermissions();
        if (this.scenariosList !== undefined) {
            // Check "Create New" permission
            if (this.userPermissionsData !== undefined && this.__getKey('create', this.userPermissionsData)) {
                this.userPermissions.create = true;
            }
            if (this.selectedScenarios.length > 0) {
                // Check "Create New" permission
                this.userPermissions.finalize = this.__checkScenariosPermission('change_status');
                // Check "Create New" permission
                this.__checkScenariosPermission('share', true);
                // Check "Create New" permission
                this.__checkScenariosPermission('copy', false, true);
                // Check "Delete" permission
                this.__checkScenariosPermission('delete');
            }
        }
    }

    __clearUserPermissions() {
        this.userPermissions.create = false;
        this.userPermissions.finalize = false;
        this.userPermissions.share = false;
        this.userPermissions.duplicate = false;
        this.userPermissions.delete = false;
    }

    __checkScenariosPermission(perm:string, check_item:boolean=false, only_one:boolean=false) {
        let curentStatus = false;
        let curentCheckCountStatus = 0;
        const selectedScenariosList = this.__getSelectedScenariosList();
        const permParamMap = {change_status: 'status', delete: 'delete', copy: 'copy', share: 'share'};
        for (const i in selectedScenariosList) {
            // console.log(perm, this.userPermissions, selectedScenariosList, this.__getKey('scenario_permission', this.__getScenario(selectedScenariosList[i]), {}));
            if (this.in_array(perm, this.__getKey('scenario_permission', this.__getScenario(selectedScenariosList[i]), {}))) {
                if (this.userPermissionsData[perm]) {
                    if (check_item) {
                        if (!this.__getKey(permParamMap[perm], this.__getScenario(selectedScenariosList[i]))) {
                            curentCheckCountStatus ++;
                        }
                    } else {
                        curentCheckCountStatus ++;
                    }
                }
            }
        }
        if (curentCheckCountStatus === selectedScenariosList.length && selectedScenariosList.length > 0) {
            if (only_one) {
                if (selectedScenariosList.length === 1) {
                    curentStatus = true;
                }
            } else {
                curentStatus = true;
            }
        }
        this.userPermissions[perm] = curentStatus;
    }
    // -------------------------------  Check permissions  -------------------------------//

    // --------------------------------  Scenario details  -------------------------------//
    __clearTableRowSelect() {
        let rows = document.getElementsByClassName('c-scenarios-table__row');
        for (let i = 0; i < rows.length; i++) {
            if (this.in_array('c-scenarios-table__row--active', rows[i].classList)) {
                rows[i].classList.remove("c-scenarios-table__row--active");
            }
        }
    }

    // Get scenario from server
    __getScenarioDetails(scenario_id: number) {
        this.req.post({
            url_id: '/forecast/get_scenario_details',
            data: {'id': scenario_id},
        }).subscribe((data) => {
            this.selectScenario = data;
        });
    }

    onSelectPreview(event: any) {
        if (this.in_array('c-scenarios-table__row', event.target.classList) || this.in_array('c-scenarios-table__row', event.target.parentNode.classList)) {
            if (this.in_array('c-scenarios-table__row', event.target.classList)) {
                this.selectElement = event.target;
            } else {
                this.selectElement = event.target.parentNode;
            }

            if (this.in_array('c-scenarios-table__row--active', this.selectElement.classList)) {
                this.selectElement.classList.remove("c-scenarios-table__row--active");
                this.selectScenario = null;
            } else {
                this.__clearTableRowSelect();
                this.selectElement.classList.add("c-scenarios-table__row--active");
                let scenario_id = parseInt(this.selectElement.attributes['data-id'].value);

                // Get scenario from server
                this.__getScenarioDetails(scenario_id);

                // Scroll to active scenario
                const selectElementHeight = this.selectElement.clientHeight;
                const selectElementPosition = this.selectElement.offsetTop;
                let tableWindowsHeight = document.getElementsByClassName('m-scenarios-page__scroll')[0].clientHeight;
                let scenariosPreview = document.getElementsByClassName('c-scenarios-preview')[0].clientHeight;
                let tableScroll = document.getElementsByClassName('m-scenarios-page__scroll')[0].scrollTop;
                tableWindowsHeight = scenariosPreview === 0 ? tableWindowsHeight - 224 : tableWindowsHeight;

                if (tableScroll > selectElementPosition - selectElementHeight) {
                    document.getElementsByClassName('m-scenarios-page__scroll')[0].scrollTop = tableScroll - selectElementHeight;
                }

                if (selectElementPosition + selectElementHeight - tableScroll > tableWindowsHeight) {
                    if (selectElementPosition > tableWindowsHeight + tableScroll) {
                        document.getElementsByClassName('m-scenarios-page__scroll')[0].scrollTop = tableScroll + 224;
                    } else {
                    document.getElementsByClassName('m-scenarios-page__scroll')[0].scrollTop = tableScroll + (selectElementPosition + selectElementHeight - tableScroll - tableWindowsHeight);
                    }
                }

                /*
                console.log(
                    'selectElementHeight', selectElementHeight,
                    'selectElementPosition', selectElementPosition,
                    'tableWindowsHeight', tableWindowsHeight,
                    'scenariosPreview', scenariosPreview,
                    'tableScroll', tableScroll
                );
                */
            }
        } else {
            event.stopPropagation();
        }

    }
    // --------------------------------  Scenario details  -------------------------------//
    onToggleScenario(event: any) {
        let element = event.target;
        if (element.checked === true) {
            this.__checkScenario(parseInt(element.attributes['data-id'].value));
        } else {
            this.__uncheckScenario(parseInt(element.attributes['data-id'].value));
        }

        let allCheckScenario = document.getElementById('sc-table-all');
        if (this.selectedScenarios.length === this.scenariosList.length) {
            allCheckScenario.checked = true;
        } else {
            allCheckScenario.checked = false;
        }

        // Check permissions
        // this.__initUserPermissions();
    }

    onToggleAllScenarios(event: any) {
        let element = event.target;
        let checked = false;
        this.selectedScenarios = [];
        if (element.checked === true) {
            checked = true;
        }

        let allElements = document.querySelectorAll('*[id^="sc-table-check-"]');
        for (let i = 0; i < allElements.length; i++) {
            allElements[i].checked = checked;
            if (checked === true) {
                this.selectedScenarios.push(allElements[i].attributes['data-id'].value);
            }
        }

        // Check permissions
        //this.__initUserPermissions();
    }

    onChangeAuthor(name: string) {
        console.log('---onChangeAuthor', name);
    } /////////////////////////////////////////////////////////////////////
    // ------------------------- ------  Scenario Actions  -------------------------------//
    __getScenario(scenario_id: number) {
        let scenario = {};
        for (const i in this.scenariosList) {
            if (this.scenariosList[i].id == scenario_id) {
                scenario = this.scenariosList[i];
                break;
            }
        }
        return scenario;
    }

    __createScenario(new_scenario: any, parent_id=null) {
        this.req.post({
            url_id: '/forecast/create_scenario',
            data: new_scenario,
        }).subscribe((data) => {
            if(!data.error) {
                let index = this.scenariosList.findIndex(x => x.id==parent_id);
                index === -1 ? index = 0 : index++;
                this.scenariosList.splice(index, 0, data);
            }
        });
    }

    __editScenario(edit_scenarios: any[]) {
        this.req.post({
            url_id: '/forecast/edit_scenario',
            data: edit_scenarios,
        }).subscribe((data) => {
            if(!data.error) {
                this.scenariosList = [];
                this.selectedScenarios = [];
                this.getScenariosList();
            }
        });
    }

    __deleteScenario(scenario_ids: number[]) {
        this.req.post({
            url_id: '/forecast/delete_scenario',
            data: {'id': scenario_ids},
        }).subscribe((data) => {
            const listStatus = new Set(Object.keys(data));
            const newScenariosList = this.scenariosList.filter(obj => !(listStatus.has(String(obj.id)) && data[String(obj.id)] === "Deleted"));
            this.scenariosList = newScenariosList;
            if (listStatus.has(String(this.selectScenario.id))) {
                this.selectScenario = null;
            }
        });
    }

    __getSelectedScenariosList() {
        let selectedScenarios = [];
        let allElements = document.querySelectorAll('*[id^="sc-table-check-"]');
        for (let i = 0; i < allElements.length; i++) {
            if (allElements[i].checked === true) {
                selectedScenarios.push(parseInt(allElements[i].attributes['data-id'].value));
            }
        }
        return selectedScenarios;
    }

    __checkScenario(id: number) {
        try {
            this.selectedScenarios.push(id);
        } catch(e) {
            console.log(e);
        }

    }

    __uncheckScenario(id: number) {
        let index = this.selectedScenarios.indexOf(id);
        if (index !== -1) {
            this.selectedScenarios.splice(index, 1);
        }
    }

    onToggleSharedScenario(event: any) {
        event.preventDefault();
        let edit_scenarios = [];
        const scenario_id = event.target.attributes['data-id'].value;
        let scenario = this.__getScenario(scenario_id);

        scenario.shared = 'Yes';

        /*
        if(this.in_array("share", scenario.scenario_permission)) {
            let new_shared = scenario.shared == 'No' ? 'Yes' : 'No';
            edit_scenarios.push({id: scenario.id, modify:[{value: new_shared, parameter: 'shared'}]});
            this.__editScenario(edit_scenarios);
        }
        */
    }

    onToggleStatusScenario(event: any) {
        event.preventDefault();
        let edit_scenarios = [];
        const scenario_id = event.target.attributes['data-id'].value;
        let scenario = this.__getScenario(scenario_id);
        if(this.in_array("change status", scenario.scenario_permission)) {
            let new_status = scenario.status == 'Final' ? 'Draft' : 'Final';
            edit_scenarios.push({id: scenario.id, modify:[{value: new_status, parameter: 'status'}]});
            this.__editScenario(edit_scenarios);
        }
    }

    onToggleFavoritScenario(event: any) {
        const edit_scenarios = [];
        const scenario_id = event.target.attributes['data-id'].value;
        let scenario = this.__getScenario(scenario_id);
        let new_favorit = scenario.favorite == 'Yes' ? 'No' : 'Yes';
        edit_scenarios.push({id: scenario.id, modify:[{value: new_favorit, parameter: 'favorite'}]});
        this.__editScenario(edit_scenarios);
    }

    onCopyScenario(event: any) {
        event.preventDefault();
        let scenario_id: number;
        try {
            scenario_id = event.target.attributes['data-id'].value;
        } catch (e) {
            scenario_id = this.selectedScenarios[0];
        }

        let scenario = this.__getScenario(scenario_id);
        if(this.in_array("copy", this.__getKey('scenario_permission', scenario))) {
            const copyScenario = {
                name: 'Copy ' + this.__getKey('name', scenario),
                description: this.__getKey('description', scenario),
                criteria: this.__getKey('criteriathis', scenario)
            };
            this.__createScenario(copyScenario, this.__getKey('id', scenario));
        }
    }

    onCloseScenariosPreview() {
        this.selectScenario = null;
        this.__clearTableRowSelect();
    }

    onDeleteScenario() {
        event.preventDefault();
        if(this.userPermissions.delete === true) {
            this.__deleteScenario(this.selectedScenarios);
        }
        // Check permissions
        this.__initUserPermissions();
    }
    // ------------------------- ------  Scenario Actions  -------------------------------//
}
