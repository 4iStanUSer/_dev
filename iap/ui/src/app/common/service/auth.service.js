"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require('@angular/core');
var Observable_1 = require('rxjs/Observable');
var UserModel = (function () {
    function UserModel() {
        this.email = null;
        this.name = null;
    }
    return UserModel;
}());
var AuthService = (function () {
    function AuthService(req) {
        this.req = req;
        /**
         * Flag for initial receiving logging status from server
         * @type {boolean}
         */
        this.initialized = false;
        /**
         * Flag of auth
         * @type {boolean}
         */
        this.is_logged_in = false;
        /**
         * Store the URL, so we can redirect after logging in
         * @type {string}
         */
        this.redirectUrl = null;
        /**
         * Store authorized user info, so we can use it for profile ...
         * @type {UserModel}
         */
        this.user = null;
        this.token = localStorage.getItem('currentUser');
        /**
         * Observable for .isLoggedIn()
         * @type {Observable<boolean>}
         */
        this.initObs = null;
        this.req.auth = this; // TODO Remake
        this.init();
    }
    /**
     * Returns observable with logged in status of user.
     * Should be used in other services/components
     * @returns {Observable<boolean>}
     */
    AuthService.prototype.isLoggedIn = function () {
        if (this.initialized)
            this.initObs = null;
        if (this.initObs) {
            return this.initObs;
        }
        else {
            /*check the localStorage for token */
            return Observable_1.Observable.of(this.is_logged_in);
        }
    };
    /**
     * Procedure of initial getting logged in status from server.
     * (!) Must be used before any other methods - catches link
     * to Request Service
     * @returns {Observable<boolean>}
     */
    AuthService.prototype.init = function () {
        var _this = this;
        //this.req = req;
        this.initObs = this.req.post({
            url_id: 'check_auth',
            sync: true,
            data: { 'X-Token': this.token }
        });
        this.initObs.subscribe(function (d) {
            _this.initialized = true;
            _this.setLoggedStatus(d);
        }, function (e) {
            _this.initialized = true;
            _this.setLoggedStatus(false);
        }, function () {
            console.log('complete  init()');
        });
        return this.initObs;
    };
    /**
     * Procedure of user's logging in. Sends request via external service.
     * If user has logged - fills all dependent own members
     * If user hasn't logged - clear all dependent own members
     * @param credentials
     * @returns {Observable<boolean>}
     */
    AuthService.prototype.login = function (credentials) {
        var _this = this;
        // return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
        var resp = this.req.post({
            url_id: 'login',
            sync: true,
            data: credentials
        });
        resp.subscribe(function (d) {
            // TODO Improve response handling
            //if (d && d['user']) {
            _this.token = d;
            _this.setLoggedStatus(true, d);
            //} else {
            //    this.setLoggedStatus(false);
            // }
        }, function (e) {
            _this.setLoggedStatus(false);
        });
        return resp;
    };
    /**
     * Procedure of user's logging out. Sends request via external service.
     * @returns {Observable<boolean>}
     */
    AuthService.prototype.logout = function () {
        var _this = this;
        var resp = this.req.post({
            url_id: 'logout',
            sync: true,
            data: {}
        });
        resp.subscribe(function (d) {
            console.log('logout success');
            _this.is_logged_in = false;
            localStorage.removeItem('currentUser');
        });
        return resp;
    };
    /**
     * Force logout
     */
    AuthService.prototype.logoutByBackend = function () {
        this.setLoggedStatus(false);
        localStorage.removeItem('currentUser');
    };
    /**
     * Low-level method of setting logging status. Has data's logic.
     * All operations of setting logged in status should use this method
     * @param status
     * @param user
     */
    AuthService.prototype.setLoggedStatus = function (status, user) {
        if (user === void 0) { user = null; }
        if (status === true) {
            this.is_logged_in = status;
            this.user = user;
            localStorage.setItem('currentUser', this.token);
            console.log("LocalStorage", localStorage.getItem('currentUser'));
        }
        else {
            this.is_logged_in = status;
            this.user = null;
            localStorage.removeItem('currentUser');
        }
    };
    AuthService = __decorate([
        core_1.Injectable()
    ], AuthService);
    return AuthService;
}());
exports.AuthService = AuthService;
