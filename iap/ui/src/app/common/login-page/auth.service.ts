import {Injectable} from '@angular/core';
import { Http, Response} from '@angular/http';
import {Location} from '@angular/common';
import {Observable} from 'rxjs/Rx';
import { AuthHttp } from 'angular2-jwt';
import { tokenNotExpired } from 'angular2-jwt';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

@Injectable()
/**
 * Service allows to check if user is authorized and adds auth token to http requests.
 * It sends login-page/logout request and stores token in local storage.
 */
export class AuthService {

    /**
     * Wrapper to get send request with token attached.
     * @type {AuthHttp}
     */

    /**
     * Key to get token from local storage.
     * @type {string}
     */
    private tokenName: string;

    /**
     * Instance of jwtHelper. Used to check if token is expired.
     * @type {jwtHelper}
     */

    constructor(private http: Http, public authHttp: AuthHttp, private location:Location) {

        this.tokenName = "token";
    }

    /**
     * Sends login-page request. If login-page successful user auth token is saved in local storage.
     * Else, function clears local storage.
     * @param username
     * @param password
     * @returns {Observable<boolean>}
     */
    login(username: string, password: string) {
        // return this.http.post('http://127.0.0.1:6543/login',
        return this.http.post('/login',
            JSON.stringify({ username: username, password: password }))
            .map(res => res.json())
            .subscribe(

                data => {
                  console.log(data);
                  localStorage.setItem('token', data.data);

                },
                error => console.log(error)
              );
    }

    /**
     * Sends logout request. Clears local storage in case of successful result.
     * @returns {Observable<boolean>}
     */
    logout() {
        this.authHttp.post('logout', '')
        .subscribe(
            data => console.log(data),
            err => console.log(err),
            () => console.log('Logout Complete')

        );

        localStorage.removeItem(this.tokenName);
    }

    /**
     * Checks if user is authenticated.
     * @returns {boolean}
     */
    isLoggedIn(): boolean {
        let token = localStorage.getItem(this.tokenName);
        if (tokenNotExpired(null, token))
        {
            return true;
        }
        else {
            localStorage.removeItem(this.tokenName);
        }
        return false;
    }
}

