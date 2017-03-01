"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require('@angular/core');
require('rxjs/add/operator/toPromise');
var USER_PERMISSION = { finalize: 'True', duplicate: 'True', delete: 'True', edit: 'True',
    create: 'True', share: 'True' };
var ScenariosListComponentService = (function () {
    function ScenariosListComponentService(req) {
        this.req = req;
        this.getScenarioPage = '/forecast/get_scenario_page';
    }
    ScenariosListComponentService.prototype.getScenariosList = function () {
        this.req.post({
            url_id: this.getScenarioPage,
            data: { 'filter': {} },
        }).subscribe(function (data) {
            console.log('*****getScenariosList', data.data);
            return data.data;
        });
    };
    ScenariosListComponentService.prototype.getUserPermissions = function () {
        return Promise.resolve(USER_PERMISSION);
    };
    ScenariosListComponentService.prototype.getScenario = function (scenario_id) {
        return null;
        //return this.getScenariosList().then(list => list.find(item => item.id == scenario_id));
    };
    ScenariosListComponentService.prototype.modifyFavorit = function (scenario_id) {
        var scenario = this.getScenario(scenario_id);
        scenario.isFavorite = !scenario.isFavorite;
        // Send to backend
    };
    ScenariosListComponentService = __decorate([
        core_1.Injectable()
    ], ScenariosListComponentService);
    return ScenariosListComponentService;
}());
exports.ScenariosListComponentService = ScenariosListComponentService;
