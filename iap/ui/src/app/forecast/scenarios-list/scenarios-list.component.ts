import { Component, OnInit} from '@angular/core';
import {AjaxService} from "../../common/service/ajax.service";

import { ScenariosListComponentService } from './scenarios-list.service';
const moment = require('moment/moment');
const DATEFORMAT = 'MM.DD.YY';


@Component({
    templateUrl: './scenarios-list.component.html',
    styleUrls: ['./scenarios-list.component.css'],
    providers: [ScenariosListComponentService]
})
export class ScenariosListComponent implements OnInit {
    scenariosList: any[];
    beforeFilterScenariosList: any[];
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

    //Filters
    filters: any = {
        favoriteCount: 0,
        sharedCount: 0,
        localCount: 0,
        finalStatusCount: 0,
        draftsStatusCount: 0,
        authorsList: [],
    };
    filterCount:any;
    filterSelect:any = {favorite:[], author:[], shared:[], status:[]};

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
        this.__getScenariosList();
        this.__loadUserPermissionsData();
        this.selectedScenarios = [];
        this.__runFilter();
    }

    ngDoCheck(): void {
        this.__initUserPermissions();
        this.__getAuthorsList();
        this.__updateFilterCount();
    }

    // Get scenarios list from server
    __getScenariosList() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.scenariosList = data.data;
            this.beforeFilterScenariosList = data.data;
        });
    }
    // ---------------------------------  Build filter  ----------------------------------//
    __getAuthorsList() {
        let authorsList = [];
        if (this.beforeFilterScenariosList !== undefined && this.beforeFilterScenariosList.length > 0) {
            for (const i in this.beforeFilterScenariosList) {
                authorsList.push(this.beforeFilterScenariosList[i].author);
            }
            authorsList = authorsList.filter((el, i, arr) => arr.indexOf(el) === i);
        }
        this.filters.authorsList = authorsList;
    }

    __maskCount(item, param){
        let filterSelectKeys = Object.keys(this.filterSelect);
        for (let k of filterSelectKeys) {
            if (k === 'shared' && param === 'shared') {
                if (this.__getKey(k, item) === 'Yes') {
                    this.filterCount['shared']++;
                } else {
                    this.filterCount['local']++;
                }
            }
            if (k === 'status' && param === 'status') {
                if (this.__getKey(k, item) === 'Final') {
                    this.filterCount['final']++;
                } else {
                    this.filterCount['drafts']++;
                }
            }
            if (k === 'favorite' && param === 'favorite') {
                if (this.__getKey(k, item) === 'Yes') {
                    this.filterCount['favorite']++;
                }
            }
        }
    }

    __updateFilterCount() {
        this.filterCount = {favorite:0, shared:0, local:0, drafts:0, final:0};
        let filterSelectKeys = Object.keys(this.filterSelect);
        for (let k of filterSelectKeys) {
            let new_mask = (JSON.parse(JSON.stringify(this.filterSelect)));
            delete new_mask[k];
            let list_scenarios:any = [];

            if (Array.isArray(this.beforeFilterScenariosList)) {
                for (let scenario of this.beforeFilterScenariosList) {
                    if (this.__maskFilter(scenario, new_mask)) {
                        list_scenarios.push(scenario);
                    }
                }
            }
            for (let item of list_scenarios) {
                this.__maskCount(item, k);
            }
        }
    }

    __maskFilter(item, mask){
        let status = true;
        if (mask !== undefined) {
            let filterSelectKeys = Object.keys(mask);
            for (let k of filterSelectKeys) {
                if (this.__getKey(k, mask).length > 0) {
                    const ind = this.__getKey(k, mask).indexOf(this.__getKey(k, item));
                    if (ind === -1) {
                        status = false;
                    }
                }
            }
        }
        return status;

    }
    __runFilter() {
        if (this.beforeFilterScenariosList !== undefined && this.beforeFilterScenariosList.length > 0) {
            this.scenariosList = [];
            for (let scenario of this.beforeFilterScenariosList) {
                if (this.__maskFilter(scenario, this.filterSelect)) {
                    this.scenariosList.push(scenario);
                }
            }
        }
        // Update Filter Count
        this.__updateFilterCount();
    }

    onChangeAuthor(event: any) {
        const value = event.target.value;
        this.filterSelect["author"] = [];
        if (value) {
            this.filterSelect["author"].push(value);
        }
        // Run filter
        this.__runFilter();
    }

    onFilter(event: any, param: string, value: string) {
        if (event.target.checked) {
            this.filterSelect[param].push(value);
        } else {
            const index = this.filterSelect[param].indexOf(value);
            if (index > -1) {
                this.filterSelect[param].splice(index, 1);
            }
        }
        // Run filter
        this.__runFilter();
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
                // Check "Finalize" permission
                this.__checkScenariosPermission('finalize', true);
                // Check "Share" permission
                this.__checkScenariosPermission('share', true);
                // Check "Copy" permission
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
        const permParamMap = {finalize: 'change_status', delete: 'delete', copy: 'copy', share: 'share'};
        for (const i in selectedScenariosList) {
            if (this.in_array(perm, this.__getKey('scenario_permission', this.__getScenario(selectedScenariosList[i]), {})) || this.in_array(permParamMap[perm], this.__getKey('scenario_permission', this.__getScenario(selectedScenariosList[i]), {}))) {
                if (this.userPermissionsData[perm]) {
                    if (check_item) {
                        if (!this.__getKey(permParamMap[perm], this.__getScenario(selectedScenariosList[i]))) {
                            if (perm === 'share') {
                                if (this.__getKey('shared', this.__getScenario(selectedScenariosList[i])) === 'No') {
                                    curentCheckCountStatus ++;
                                }
                            } else if (perm === 'finalize') {
                                if (this.__getKey('status', this.__getScenario(selectedScenariosList[i])) === 'Draft') {
                                    curentCheckCountStatus ++;
                                }
                            } else {
                                curentCheckCountStatus ++;
                            }
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

    // ------------------------- ------  Scenario Actions  -------------------------------//
    __getScenario(scenario_id: number) {
        let scenario = {};
        for (const i in this.scenariosList) {
            if (this.scenariosList[i].id == scenario_id) {
                scenario = this.scenariosList[i];
                return scenario;
            }
        }
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
            for (let i = 0; i < data.length; i++) {
                for(let j = 0; j < data[i].modified.length; j++) {
                    if ( data[i].modified[j].status === true) {
                        for (const k in this.scenariosList) {
                            if (this.scenariosList[k].id == data[i].id) {
                                this.scenariosList[k][data[i].modified[j].parameter] = data[i].modified[j].value;
                                break;
                            }
                        }
                    }
                }
            }
            // Update user permissions
            this.__initUserPermissions();
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
        let allElements:any = document.querySelectorAll('*[id^="sc-table-check-"]');
        for (let i = 0; i < allElements.length; i++) {
            if (allElements[i].checked === true) {
                selectedScenarios.push(parseInt(allElements[i].attributes['data-id'].value));
            }
        }
        return selectedScenarios;
    }

    __checkScenario(id: number) {
        try {
            const index = this.selectedScenarios.indexOf(id);
            if (index === -1) {
                this.selectedScenarios.push(id);
            }
        } catch(e) {
            console.log(e);
        }

    }

    __uncheckScenario(id: number) {
        const index = this.selectedScenarios.indexOf(id);
        if (index !== -1) {
            this.selectedScenarios.splice(index, 1);
        }
    }

    onToggleScenario(event:any) {
        let element: any = event.target;
        if (element.checked === true) {
            this.__checkScenario(parseInt(element.attributes['data-id'].value));
        } else {
            this.__uncheckScenario(parseInt(element.attributes['data-id'].value));
        }

        let allCheckScenario:any = document.getElementById('sc-table-all');
        if (this.selectedScenarios.length === this.scenariosList.length) {
            allCheckScenario.checked = true;
        } else {
            allCheckScenario.checked = false;
        }
    }

    onToggleAllScenarios(event:any) {
        let element = event.target;
        let checked = false;
        this.selectedScenarios = [];
        if (element.checked === true) {
            checked = true;
        }

        let allElements:any = document.querySelectorAll('*[id^="sc-table-check-"]');
        for (let i = 0; i < allElements.length; i++) {
            allElements[i].checked = checked;
            if (checked === true) {
                this.selectedScenarios.push(parseInt(allElements[i].attributes['data-id'].value));
            }
        }
    }

    onToggleSharedScenario(event: any) {
        event.preventDefault();
        let edit_scenarios = [];
        let e_scenarios = [];

        try {
            const scenario_id = event.target.attributes['data-id'].value;
            e_scenarios.push(scenario_id);
        } catch (e) {
            if (this.__getKey('share', this.userPermissions) === true) {
                e_scenarios = this.selectedScenarios;
            }
        }
        if (e_scenarios.length > 0) {
            for (let i = 0; i < e_scenarios.length; i++) {
                const scenario = this.__getScenario(e_scenarios[i]);
                if (this.in_array("share", this.__getKey('scenario_permission', scenario))) {
                    let new_shared = this.__getKey('shared', scenario) === 'No' ? 'Yes' : 'No';
                    edit_scenarios.push({
                        id: this.__getKey('id', scenario),
                        modify: [{value: new_shared, parameter: 'shared'}]
                    });
                }
            }
            if (edit_scenarios.length > 0) {
                this.__editScenario(edit_scenarios);
            }
        }
    }

    onToggleStatusScenario(event: any) {
        event.preventDefault();
        let edit_scenarios = [];
        let e_scenarios = [];

        try {
            const scenario_id = event.target.attributes['data-id'].value;
            e_scenarios.push(scenario_id);
        } catch (e) {
            if (this.__getKey('finalize', this.userPermissions) === true) {
                e_scenarios = this.selectedScenarios;
            }
        }

        if (e_scenarios.length > 0) {
            for (let i = 0; i < e_scenarios.length; i++) {
                const scenario = this.__getScenario(e_scenarios[i]);
                if (this.in_array("change_status", this.__getKey('scenario_permission', scenario))) {
                    let new_status = this.__getKey('status', scenario) === 'Final' ? 'Draft' : 'Final';
                    edit_scenarios.push({
                        id: this.__getKey('id', scenario),
                        modify: [{value: new_status, parameter: 'status'}]
                    });
                }
            }
            if (edit_scenarios.length > 0) {
                this.__editScenario(edit_scenarios);
            }
        }
    }

    onToggleFavoritScenario(event: any) {
        event.preventDefault();
        const edit_scenarios = [];
        const scenario_id = event.target.attributes['data-id'].value;
        let scenario = this.__getScenario(scenario_id);
        let new_favorit = this.__getKey('favorite', scenario) === 'Yes' ? 'No' : 'Yes';
        edit_scenarios.push({id: this.__getKey('id', scenario), modify:[{value: new_favorit, parameter: 'favorite'}]});
        this.__editScenario(edit_scenarios);
    }

    onCopyScenario(event: any) {
        event.preventDefault();
        let scenario_id: number;
        try {
            scenario_id = event.target.attributes['data-id'].value;
        } catch (e) {
            if (this.__getKey('copy', this.userPermissions) === true) {
                scenario_id = this.selectedScenarios[0];
            }
        }

        let scenario = this.__getScenario(scenario_id);
        if (scenario) {
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

    onDeleteScenario(event: any) {
        event.preventDefault();
        if(this.__getKey('delete', this.userPermissions) === true) {
            this.__deleteScenario(this.selectedScenarios);
        }
        // Update user permissions
        this.__initUserPermissions();
    }
    // ------------------------- ------  Scenario Actions  -------------------------------//
}
