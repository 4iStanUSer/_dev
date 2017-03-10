import { Component, OnInit} from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';


import {AjaxService} from "../../../common/service/ajax.service";
import {ScenarioDetailsModel, ScenarioModel} from "../scenario.model";
import {ScenarioService} from "../scenario.service";


const moment = require('moment/moment');
const MIN_SEARCH_LENGTH = 3;
const DATEFORMAT = 'MM.DD.YY';
const SORTING_FIELD = 'name';
const SORTING_ORDER = true; //true == 'ASC', false == 'DESC'


@Component({
    templateUrl: './scenarios-list.component.html',
    styleUrls: ['../scenarios.component.css'],
})

export class ScenariosListComponent implements OnInit {
    scenariosList: any[];
    beforeFilterScenariosList: any[];
    userPermissionsData: any[];
    selectedScenarios: any[];
    work_list: any[];
    favoriteList: any;
    selectElement: any;
    selectScenario: ScenarioDetailsModel;
    sorting: any = {field: SORTING_FIELD, order: SORTING_ORDER};

    //Permissions
    userPermissions: any = {
        create: false,
        finalize: false,
        share: false,
        edit: false,
        copy: false,
        delete: false
    };

    // Multiselect
    multiselect: any = {
        active: false,
        selected: []
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
    filterCount:any = {favorite:0, shared:0, local:0, drafts:0, final:0};
    filterSelect:any = {favorite:[], author:[], shared:[], status:[], search: ''};

    constructor(
        private router: Router,
        private req: AjaxService,
        private route: ActivatedRoute,
        private scenarioService: ScenarioService
    ) { }

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

    __sortByKey() {
        const self = this;
        console.log('--------------------__sortByKey', self.sorting);
        if (self.scenariosList !== undefined && self.scenariosList.length > 0) {
            return self.scenariosList.sort(function (a, b) {
                let x = a[self.sorting.field];
                let y = b[self.sorting.field];

                if (typeof x == "string") {
                    x = x.toLowerCase();
                }
                if (typeof y == "string") {
                    y = y.toLowerCase();
                }
                if (self.sorting.order === true) {
                    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
                } else {
                    return ((x > y) ? -1 : ((x < y) ? 1 : 0));
                }
            });
        }
    }

    in_array(what, where) {
        for(var i=0; i<where.length; i++)
            if(what === where[i])
                return true;
        return false;
    }

    ngOnInit(): void {
        // First load data
        this.__getScenariosList();
        // Update user permissions
        this.__loadUserPermissionsData();
        this.selectedScenarios = [];
    }

    ngDoCheck(): void {
        this.__initUserPermissions();
        this.__getAuthorsList();
    }

    // Get scenarios list from server
    __getScenariosList() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.scenariosList = data.data;
            this.beforeFilterScenariosList = data.data;
            // Get work list
            this.__getWorkList();
            // First filter scenarios
            this.__runFilter();
            // Update filter count
            this.__updateFilterCount();
            // First sorting scenarios
            this.__sortByKey();
        });
    }

    // Get work list
    __getWorkList() {
        let work_list = [];
        if (this.beforeFilterScenariosList !== undefined && this.beforeFilterScenariosList.length > 0) {
            work_list = this.beforeFilterScenariosList.filter(item => this.__getKey('favorite', item) === 'Yes');
        }
        this.work_list = work_list;
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
        console.log('--------------------__updateFilterCount', this.filterSelect);
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
                    if (k === 'search') {
                        if (this.__getKey('name', item).toLowerCase().search(this.__getKey(k, mask)) === -1 && this.__getKey('description', item).toLowerCase().search(this.__getKey(k, mask)) === -1) {
                            status = false;
                        }
                    } else {
                        const ind = this.__getKey(k, mask).indexOf(this.__getKey(k, item));
                        if (ind === -1) {
                            status = false;
                        }
                    }
                }
            }
        }
        return status;

    }
    __runFilter() {
        console.log('--------------------__runFilter', this.filterSelect);
        if (this.beforeFilterScenariosList !== undefined && this.beforeFilterScenariosList.length > 0) {
            this.scenariosList = [];
            for (let scenario of this.beforeFilterScenariosList) {
                if (this.__maskFilter(scenario, this.filterSelect)) {
                    this.scenariosList.push(scenario);
                }
            }
        }
    }

    onChangeAuthor(event: any) {
        const value = event.target.value;
        this.filterSelect["author"] = [];
        if (value) {
            this.filterSelect["author"].push(value);
        }
        this.__runFilter();
        this.__updateFilterCount();
        this.__sortByKey();
    }

    onChangeSearch(event: any) {
        const value = event.target.value;
        if (MIN_SEARCH_LENGTH <= value.length) {
            this.filterSelect["search"] = value.toLowerCase();
        } else {
            this.filterSelect["search"] = '';
        }
        this.__runFilter();
        this.__updateFilterCount();
        this.__sortByKey();
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
        this.__runFilter();
        this.__updateFilterCount();
        this.__sortByKey();
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
            if (this.userPermissionsData !== undefined ) {
                if (this.__getKey('create', this.userPermissionsData) === true) {
                    this.userPermissions.create = true;
                }
                if (this.__getKey('edit', this.userPermissionsData) === true) {
                    this.userPermissions.edit = true;
                }
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
    __getScenarioDetails(scenario_id: number): void {
        this.selectScenario = this.scenarioService.getScenarioDetails(scenario_id);
        console.log('--------------__getScenarioDetails', this.selectScenario);
    }

    onSelectPreview(event: any) {
        event.stopPropagation();
        if (!this.multiselect.active) {
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
            }
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
            // Update scenarios list
            this.__getScenariosList();

            // Update user permissions
            this.__initUserPermissions();

            // Update filter count
            this.__updateFilterCount();

            //
            // this.__runFilter();
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

        // Update scenarios list
        this.__getScenariosList();

        // Run filter
        this.__runFilter();

        // Update user permissions
        this.__initUserPermissions();

        // Update filter count
        this.__updateFilterCount();
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

    onToggleMultiselect(event:any) {
        let element = event.target;
        element.checked = !this.multiselect.active;
        this.multiselect.active = !this.multiselect.active;
        this.selectedScenarios = [];
        this.onCloseScenariosPreview();
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
        if (!this.multiselect.active) {
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
    }

    onToggleStatusScenario(event: any) {
        event.preventDefault();
        if (!this.multiselect.active) {
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
    }

    onToggleSort(field: string) {
        if (field !== this.sorting.field) {
            this.sorting['field'] = field;
            this.sorting['order'] = true;
        } else {
            this.sorting.order = !this.sorting.order;
        }

        // Run new sorting
        this.__sortByKey();
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
        if (!this.multiselect.active) {
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
    }

    goToEditScenario(event: any) {
        event.preventDefault();
        if (!this.multiselect.active) {
            if (this.__getKey('edit', this.userPermissions) === true) {
                const scenario_id = event.target.attributes['data-id'].value;
                const scenario = this.__getScenario(scenario_id);
                if (this.in_array("edit", this.__getKey('scenario_permission', scenario))) {
                    this.router.navigate(["../edit-scenario", this.__getKey('id', scenario)], {relativeTo: this.route});
                }
            }
        }
    }

    goToSimulator(event: any) {
        event.preventDefault();
        if (!this.multiselect.active) {
            // TODO Add run simulator
            const scenario_id = event.target.attributes['data-id'].value;
            this.router.navigate(["../../simulator"], {relativeTo: this.route});
        }
    }

    goToNewScenario(event: any) {
        event.preventDefault();
        if(this.__getKey('create', this.userPermissions) === true) {
            this.router.navigate(["../new-scenario"], { relativeTo: this.route });
        }
    }
    // ------------------------- ------  Scenario Actions  -------------------------------//
}
