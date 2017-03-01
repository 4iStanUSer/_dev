"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require('@angular/core');
var LoadingService = (function () {
    function LoadingService() {
        this.queue = [];
    }
    LoadingService.prototype.show = function (id) {
        if (this.queue.indexOf(id) == -1) {
            this.queue.push(id);
            console.log('---show loading');
        }
        else {
            console.warn('process ' + id + ' already exists in queue!');
        }
    };
    LoadingService.prototype.hide = function (id) {
        var index = this.queue.indexOf(id);
        if (index != -1) {
            this.queue.splice(index, 1);
        }
        if (this.queue.length == 0) {
            console.log('---hide loading');
        }
    };
    LoadingService.prototype.getQueue = function () {
        return this.queue;
    };
    LoadingService = __decorate([
        core_1.Injectable()
    ], LoadingService);
    return LoadingService;
}());
exports.LoadingService = LoadingService;
