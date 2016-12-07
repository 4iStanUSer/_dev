import {Injectable} from '@angular/core';

import {Observable} from 'rxjs/Observable';

import {AjaxService} from "./ajax.service";

class UserModel {
    email: string = null;
    name: string = null;
}

@Injectable()
/**
 * Service to store user's authentication status and all  related information:
 * - user profile,
 * - requests for login/logout,
 * - request for initial status
 * Main method - .isLoggedIn() - is used for checking status
 */
export class AuthService {

    /**
     * Flag for initial receiving logging status from server
     * @type {boolean}
     */
    private initialized: boolean = false;

    /**
     * Flag of auth
     * @type {boolean}
     */
    private is_logged_in = false;

    /**
     * Store the URL, so we can redirect after logging in
     * @type {string}
     */
    redirectUrl: string = null;

    /**
     * Store authorized user info, so we can use it for profile ...
     * @type {UserModel}
     */
    user: UserModel = null;

    /**
     * Observable for .isLoggedIn()
     * @type {Observable<boolean>}
     */
    private initObs: Observable<boolean> = null;

    constructor(private req: AjaxService) {
        this.req.auth = this; // TODO Remake
        this.init();
    }

    /**
     * Returns observable with logged in status of user.
     * Should be used in other services/components
     * @returns {Observable<boolean>}
     */
    isLoggedIn(): Observable<boolean> {

        if (this.initialized) this.initObs = null;
        if (this.initObs) {
            return this.initObs;
        } else {
            return Observable.of(this.is_logged_in);
        }
    }

    /**
     * Procedure of initial getting logged in status from server.
     * (!) Must be used before any other methods - catches link
     * to Request Service
     * @returns {Observable<boolean>}
     */
    init(): Observable<boolean> {
        //this.req = req;
        this.initObs = this.req.get({
            url_id: 'check_auth',
            sync: true,
            data: {}
        });
        this.initObs.subscribe(
            (d) => {
                this.initialized = true;
                this.setLoggedStatus(d);
            },
            (e) => {
                this.initialized = true;
                this.setLoggedStatus(false);
            },
            () => {
                console.log('complete  init()');
            }
        );
        return this.initObs;
    }

    /**
     * Procedure of user's logging in. Sends request via external service.
     * If user has logged - fills all dependent own members
     * If user hasn't logged - clear all dependent own members
     * @param credentials
     * @returns {Observable<boolean>}
     */
    login(credentials: Object): Observable<boolean> {
        // return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
        let resp = this.req.get({
            url_id: 'login',
            sync: true,
            data: credentials
        });
        resp.subscribe(
            (d) => {
                // TODO Improve response handling
                if (d && d['logged']) {
                    this.setLoggedStatus(true, d['user']);
                } else {
                    this.setLoggedStatus(false);
                }
            },
            (e) => {
                this.setLoggedStatus(false);
            }
        );
        return resp;
    }

    /**
     * Procedure of user's logging out. Sends request via external service.
     * @returns {Observable<boolean>}
     */
    logout(): Observable<boolean> {
        let resp = this.req.get({
            url_id: 'logout',
            sync: true,
            data: {}
        });
        resp.subscribe((d) => {
            console.log('logout success');
            this.is_logged_in = false;
        });
        return resp;
    }

    /**
     * Force logout
     */
    logoutByBackend() {
        this.setLoggedStatus(false);
    }

    /**
     * Low-level method of setting logging status. Has data's logic.
     * All operations of setting logged in status should use this method
     * @param status
     * @param user
     */
    private setLoggedStatus(status: boolean, user: UserModel = null) {
        if (status === true) {
            this.is_logged_in = status;
            this.user = user;
        } else {
            this.is_logged_in = status;
            this.user = null;
        }
    }
}
