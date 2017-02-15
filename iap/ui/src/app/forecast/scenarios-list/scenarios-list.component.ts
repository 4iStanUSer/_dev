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
    user_permissions: any;
    selectedScenarios: any[];
    favoriteList: any;
    selectElement: any;
    selectScenario: any;
    search: string;

    //Permissions
    createNewPermissionStatus:boolean = false;
    finalizePermissionStatus:boolean = false;
    sharePermissionStatus:boolean = false;
    duplicatePermissionStatus:boolean = false;
    deletePermissionStatus:boolean = false;

    constructor(private req: AjaxService) { }

    // Parse date 2017-02-10 14:00:13.990018 to DATEFORMAT
    dateParse(dateString: string) {
        return moment(Date.parse(dateString)).format(DATEFORMAT);
    }

    in_array(what, where) {
        for(var i=0; i<where.length; i++)
            if(what === where[i])
                return true;
        return false;
    }

    __getScenario(id: any) {
        let scenario = null;
        for (const i in this.scenariosList) {
            if (this.scenariosList[i].id === parseInt(id)) {
                scenario = this.scenariosList[i];
                break;
            }
        }
        return scenario;
    }

    __clearTableRowSelect() {
        let rows = document.getElementsByClassName('c-scenarios-table__row');
        for (let i = 0; i < rows.length; i++) {
            if (this.in_array('c-scenarios-table__row--active', rows[i].classList)) {
                rows[i].classList.remove("c-scenarios-table__row--active");
            }
        }
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

    // Get ScenariosList from Service
    getScenariosList() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.scenariosList = data.data;
        });
    }
    getUserPermissions() {
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: {'filter': {}},
        }).subscribe((data) => {
            this.user_permissions = data.user_permission;
        });
    }

    ngOnInit(): void {
        this.getScenariosList();
        this.getUserPermissions();
        this.selectedScenarios = [];
    }

    ngDoCheck(): void {
        this.checkSharePermission();
        this.getFavoriteList();
        this.getSharedCount();
        this.getLocalCount();
        this.getFinalStatusCount();
        this.getDraftsStatusCount();
        this.getAuthorsList();

        // Check permissions
        this.checkCreateNewPermissionStatus();
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
                if (this.scenariosList[i].isFavorite === true) {
                    this.favoriteList.push(this.scenariosList[i].id);
                }
            }
        }
    }

    getSharedCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const sharedList = this.scenariosList.filter((item) => {
                return item.shared == 'True'
            });
            return sharedList.length;
        } else {
            return 0;
        }
    }

    getLocalCount() {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            const localList = this.scenariosList.filter((item) => {
                return item.shared == 'False'
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
    checkCreateNewPermissionStatus() {
        this.createNewPermissionStatus = false;
        if (this.user_permissions !== undefined && this.user_permissions.create) {
            this.createNewPermissionStatus = true;
        }
    }
    checkFinalizePermissionStatus() {
        this.finalizePermissionStatus = false;
        let curentFinalizePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (const i in this.selectedScenarios) {
                if (this.in_array('change status', this.__getScenario(this.selectedScenarios[i]).scenario_permission) && this.__getScenario(this.selectedScenarios[i]).status.toLowerCase() !== 'final') {
                    if (this.user_permissions !== undefined && this.user_permissions.finalize === 'True') {
                        curentFinalizePermissionStatus ++;
                    }
                }
            }
            if (curentFinalizePermissionStatus === this.selectedScenarios.length) {
                this.finalizePermissionStatus = true;
            }
        }
    }
    checkSharePermission() {
        this.sharePermissionStatus = false;
        let curentSharePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (const i in this.selectedScenarios) {
                if (this.in_array('share', this.__getScenario(this.selectedScenarios[i]).scenario_permission) && !this.__getScenario(this.selectedScenarios[i]).shared) {
                    if (this.user_permissions !== undefined && this.user_permissions.share) {
                        curentSharePermissionStatus ++;
                    }
                }
            }
            if (curentSharePermissionStatus === this.selectedScenarios.length) {
                this.sharePermissionStatus = true;
            }
        }
    }
    checkDuplicatePermission() {
        this.duplicatePermissionStatus = false;
        let curentDuplicatePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (const i in this.selectedScenarios) {
                if (this.in_array('copy', this.__getScenario(this.selectedScenarios[i]).scenario_permission)) {
                    if (this.user_permissions !== undefined && this.user_permissions.duplicate === 'True') {
                        curentDuplicatePermissionStatus ++;
                    }
                }
            }
            if (curentDuplicatePermissionStatus === this.selectedScenarios.length) {
                this.duplicatePermissionStatus = true;
            }
        }
    }
    checkDeletePermission() {
        this.deletePermissionStatus = false;
        let curentDeletePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (const i in this.selectedScenarios) {
                if (this.in_array('delete', this.__getScenario(this.selectedScenarios[i]).scenario_permission)) {
                    if (this.user_permissions !== undefined && this.user_permissions.delete === 'True') {
                        curentDeletePermissionStatus ++;
                    }
                }
            }
            if (curentDeletePermissionStatus === this.selectedScenarios.length) {
                this.deletePermissionStatus = true;
            }
        }
    }
    // -------------------------------  Check permissions  -------------------------------//

    onToggleScenario(event: any) {
        let element = event.target;
        if (element.checked === true) {
            this.__checkScenario(element.attributes['data-id'].value);
        } else {
            this.__uncheckScenario(element.attributes['data-id'].value);
        }

        let allCheckScenario = document.getElementById('sc-table-all');
        if (this.selectedScenarios.length === this.scenariosList.length) {
            allCheckScenario.checked = true;
        } else {
            allCheckScenario.checked = false;
        }

        // Check permissions
        this.checkSharePermission();
        this.checkFinalizePermissionStatus();
        this.checkDuplicatePermission();
        this.checkDeletePermission();
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
        this.checkSharePermission();
        this.checkFinalizePermissionStatus();
        this.checkDuplicatePermission();
        this.checkDeletePermission();
    }

    onToggleFavoritScenario(event: any) {
        let scenario_id = event.target.attributes['data-id'].value;
        console.log('---onToggleFavoritScenario', scenario_id);
        this.scenariosListComponentService.modifyFavorit(scenario_id);
    }

    onChangeAuthor(name: string) {
        console.log('---onChangeAuthor', name);
    }

    onCopyScenario(event: any) {
        event.preventDefault();
        let scenario_id = event.target.attributes['data-id'].value;
        let curent_scenario = this.scenariosListComponentService.getScenario(scenario_id);
        console.log('---onCopyScenario', curent_scenario);
        if (this.in_array('copy', curent_scenario.scenario_permission)) {
            console.log(curent_scenario);
        }
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
                let scenario_id = this.selectElement.attributes['data-id'].value;

                //
                console.log('---onSelectPreview', this.selectScenario);
                this.selectScenario = this.scenariosListComponentService.getScenario(scenario_id);
            }

        } else {
            event.stopPropagation();
        }

    }

    onCloseScenariosPreview(event: any) {
        this.selectScenario = null;
        this.__clearTableRowSelect();
    }
}
