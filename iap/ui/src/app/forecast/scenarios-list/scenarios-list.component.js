"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require('@angular/core');
var scenarios_list_service_1 = require('./scenarios-list.service');
// import lowerCase = require("lower-case");
var moment = require('moment/moment');
var DATEFORMAT = 'MM.DD.YY';
var ScenariosListComponent = (function () {
    function ScenariosListComponent(req) {
        this.req = req;
        //Permissions
        this.createNewPermissionStatus = false;
        this.finalizePermissionStatus = false;
        this.sharePermissionStatus = false;
        this.duplicatePermissionStatus = false;
        this.deletePermissionStatus = false;
    }
    // Parse date 2017-02-10 14:00:13.990018 to DATEFORMAT
    ScenariosListComponent.prototype.dateParse = function (dateString) {
        return moment(Date.parse(dateString)).format(DATEFORMAT);
    };
    ScenariosListComponent.prototype.in_array = function (what, where) {
        for (var i = 0; i < where.length; i++)
            if (what === where[i])
                return true;
        return false;
    };
    ScenariosListComponent.prototype.__getScenario = function (id) {
        var scenario = null;
        for (var i in this.scenariosList) {
            if (this.scenariosList[i].id === parseInt(id)) {
                scenario = this.scenariosList[i];
                break;
            }
        }
        return scenario;
    };
    ScenariosListComponent.prototype.__clearTableRowSelect = function () {
        var rows = document.getElementsByClassName('c-scenarios-table__row');
        for (var i = 0; i < rows.length; i++) {
            if (this.in_array('c-scenarios-table__row--active', rows[i].classList)) {
                rows[i].classList.remove("c-scenarios-table__row--active");
            }
        }
    };
    ScenariosListComponent.prototype.__checkScenario = function (id) {
        try {
            this.selectedScenarios.push(id);
        }
        catch (e) {
            console.log(e);
        }
    };
    ScenariosListComponent.prototype.__uncheckScenario = function (id) {
        var index = this.selectedScenarios.indexOf(id);
        if (index !== -1) {
            this.selectedScenarios.splice(index, 1);
        }
    };
    // Get scenarios list from server
    ScenariosListComponent.prototype.getScenariosList = function () {
        var _this = this;
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: { 'filter': {} },
        }).subscribe(function (data) {
            _this.scenariosList = data.data;
        });
    };
    // Get user permissions from server
    ScenariosListComponent.prototype.getUserPermissions = function () {
        var _this = this;
        this.req.post({
            url_id: '/forecast/get_scenario_page',
            data: { 'filter': {} },
        }).subscribe(function (data) {
            _this.user_permissions = data.user_permission;
        });
    };
    // Get scenario from server
    ScenariosListComponent.prototype.getScenarioDetails = function (scenario_id) {
        var _this = this;
        this.req.post({
            url_id: '/get_scenario_details',
            data: { 'id': scenario_id },
        }).subscribe(function (data) {
            _this.selectScenario = data;
        });
    };
    ScenariosListComponent.prototype.ngOnInit = function () {
        this.getScenariosList();
        this.getUserPermissions();
        this.selectedScenarios = [];
    };
    ScenariosListComponent.prototype.ngDoCheck = function () {
        this.checkSharePermission();
        this.getFavoriteList();
        this.getSharedCount();
        this.getLocalCount();
        this.getFinalStatusCount();
        this.getDraftsStatusCount();
        this.getAuthorsList();
        // Check permissions
        this.checkCreateNewPermissionStatus();
    };
    // ---------------------------------  Build filter  ----------------------------------//
    ScenariosListComponent.prototype.getFavoriteListLength = function () {
        try {
            return this.favoriteList.length;
        }
        catch (e) {
            return 0;
        }
    };
    ScenariosListComponent.prototype.getFavoriteList = function () {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            this.favoriteList = [];
            for (var i = 0; i < this.scenariosList.length; i++) {
                if (this.scenariosList[i].isFavorite === true) {
                    this.favoriteList.push(this.scenariosList[i].id);
                }
            }
        }
    };
    ScenariosListComponent.prototype.getSharedCount = function () {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            var sharedList = this.scenariosList.filter(function (item) {
                return item.shared.toLowerCase() === 'yes';
            });
            return sharedList.length;
        }
        else {
            return 0;
        }
    };
    ScenariosListComponent.prototype.getLocalCount = function () {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            var localList = this.scenariosList.filter(function (item) {
                return item.shared.toLowerCase() === 'no';
            });
            return localList.length;
        }
        else {
            return 0;
        }
    };
    ScenariosListComponent.prototype.getFinalStatusCount = function () {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            var finalStatusList = this.scenariosList.filter(function (item) {
                return item.status.toLowerCase() == 'final';
            });
            return finalStatusList.length;
        }
        else {
            return 0;
        }
    };
    ScenariosListComponent.prototype.getDraftsStatusCount = function () {
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            var draftsStatusList = this.scenariosList.filter(function (item) {
                return item.status.toLowerCase() == 'draft';
            });
            return draftsStatusList.length;
        }
        else {
            return 0;
        }
    };
    ScenariosListComponent.prototype.getAuthorsList = function () {
        var authorsList = [];
        if (this.scenariosList !== undefined && this.scenariosList.length > 0) {
            for (var i in this.scenariosList) {
                authorsList.push(this.scenariosList[i].author);
            }
            return authorsList.filter(function (el, i, arr) { return arr.indexOf(el) === i; });
        }
    };
    // ---------------------------------  Build filter  ----------------------------------//
    // -------------------------------  Check permissions  -------------------------------//
    ScenariosListComponent.prototype.checkCreateNewPermissionStatus = function () {
        this.createNewPermissionStatus = false;
        if (this.user_permissions !== undefined && this.user_permissions.create) {
            this.createNewPermissionStatus = true;
        }
    };
    ScenariosListComponent.prototype.checkFinalizePermissionStatus = function () {
        this.finalizePermissionStatus = false;
        var curentFinalizePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (var i in this.selectedScenarios) {
                if (this.in_array('change status', this.__getScenario(this.selectedScenarios[i]).scenario_permission) && this.__getScenario(this.selectedScenarios[i]).status.toLowerCase() !== 'final') {
                    if (this.user_permissions !== undefined && this.user_permissions.finalize) {
                        curentFinalizePermissionStatus++;
                    }
                }
            }
            if (curentFinalizePermissionStatus === this.selectedScenarios.length) {
                this.finalizePermissionStatus = true;
            }
        }
    };
    ScenariosListComponent.prototype.checkSharePermission = function () {
        this.sharePermissionStatus = false;
        var curentSharePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (var i in this.selectedScenarios) {
                if (this.in_array('share', this.__getScenario(this.selectedScenarios[i]).scenario_permission) && !this.__getScenario(this.selectedScenarios[i]).shared) {
                    if (this.user_permissions !== undefined && this.user_permissions.share) {
                        curentSharePermissionStatus++;
                    }
                }
            }
            if (curentSharePermissionStatus === this.selectedScenarios.length) {
                this.sharePermissionStatus = true;
            }
        }
    };
    ScenariosListComponent.prototype.checkDuplicatePermission = function () {
        this.duplicatePermissionStatus = false;
        var curentDuplicatePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (var i in this.selectedScenarios) {
                if (this.in_array('copy', this.__getScenario(this.selectedScenarios[i]).scenario_permission)) {
                    if (this.user_permissions !== undefined && this.user_permissions.duplicate) {
                        curentDuplicatePermissionStatus++;
                    }
                }
            }
            if (curentDuplicatePermissionStatus === this.selectedScenarios.length && this.selectedScenarios.length === 1) {
                this.duplicatePermissionStatus = true;
            }
        }
    };
    ScenariosListComponent.prototype.checkDeletePermission = function () {
        this.deletePermissionStatus = false;
        var curentDeletePermissionStatus = 0;
        if (this.selectedScenarios.length > 0) {
            for (var i in this.selectedScenarios) {
                if (this.in_array('delete', this.__getScenario(this.selectedScenarios[i]).scenario_permission)) {
                    if (this.user_permissions !== undefined && this.user_permissions.delete) {
                        curentDeletePermissionStatus++;
                    }
                }
            }
            if (curentDeletePermissionStatus === this.selectedScenarios.length) {
                this.deletePermissionStatus = true;
            }
        }
    };
    // -------------------------------  Check permissions  -------------------------------//
    // --------------------------------  Scenario details  -------------------------------//
    ScenariosListComponent.prototype.onSelectPreview = function (event) {
        if (this.in_array('c-scenarios-table__row', event.target.classList) || this.in_array('c-scenarios-table__row', event.target.parentNode.classList)) {
            if (this.in_array('c-scenarios-table__row', event.target.classList)) {
                this.selectElement = event.target;
            }
            else {
                this.selectElement = event.target.parentNode;
            }
            if (this.in_array('c-scenarios-table__row--active', this.selectElement.classList)) {
                this.selectElement.classList.remove("c-scenarios-table__row--active");
                this.selectScenario = null;
            }
            else {
                this.__clearTableRowSelect();
                this.selectElement.classList.add("c-scenarios-table__row--active");
                var scenario_id = parseInt(this.selectElement.attributes['data-id'].value);
                // Get scenario from server
                this.getScenarioDetails(scenario_id);
            }
        }
        else {
            event.stopPropagation();
        }
    };
    // --------------------------------  Scenario details  -------------------------------//
    ScenariosListComponent.prototype.onToggleScenario = function (event) {
        var element = event.target;
        if (element.checked === true) {
            this.__checkScenario(element.attributes['data-id'].value);
        }
        else {
            this.__uncheckScenario(element.attributes['data-id'].value);
        }
        var allCheckScenario = document.getElementById('sc-table-all');
        if (this.selectedScenarios.length === this.scenariosList.length) {
            allCheckScenario.checked = true;
        }
        else {
            allCheckScenario.checked = false;
        }
        // Check permissions
        this.checkSharePermission();
        this.checkFinalizePermissionStatus();
        this.checkDuplicatePermission();
        this.checkDeletePermission();
    };
    ScenariosListComponent.prototype.onToggleAllScenarios = function (event) {
        var element = event.target;
        var checked = false;
        this.selectedScenarios = [];
        if (element.checked === true) {
            checked = true;
        }
        var allElements = document.querySelectorAll('*[id^="sc-table-check-"]');
        for (var i = 0; i < allElements.length; i++) {
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
    };
    ScenariosListComponent.prototype.onToggleFavoritScenario = function (event) {
        var scenario_id = event.target.attributes['data-id'].value;
        console.log('---onToggleFavoritScenario', scenario_id);
        this.scenariosListComponentService.modifyFavorit(scenario_id);
    };
    ScenariosListComponent.prototype.onChangeAuthor = function (name) {
        console.log('---onChangeAuthor', name);
    };
    ScenariosListComponent.prototype.onCopyScenario = function (event) {
        event.preventDefault();
        var scenario_id = event.target.attributes['data-id'].value;
        var curent_scenario = this.scenariosListComponentService.getScenario(scenario_id);
        console.log('---onCopyScenario', curent_scenario);
        if (this.in_array('copy', curent_scenario.scenario_permission)) {
            console.log(curent_scenario);
        }
    };
    ScenariosListComponent.prototype.onCloseScenariosPreview = function (event) {
        this.selectScenario = null;
        this.__clearTableRowSelect();
    };
    ScenariosListComponent = __decorate([
        core_1.Component({
            templateUrl: './scenarios-list.component.html',
            styleUrls: ['./scenarios-list.component.css'],
            providers: [scenarios_list_service_1.ScenariosListComponentService]
        })
    ], ScenariosListComponent);
    return ScenariosListComponent;
}());
exports.ScenariosListComponent = ScenariosListComponent;
