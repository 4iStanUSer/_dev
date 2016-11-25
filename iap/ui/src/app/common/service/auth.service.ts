import {Injectable} from '@angular/core';

import { Observable } from 'rxjs/Observable';

class UserModel {
    email: string;
    name: string;
}

@Injectable()
export class AuthService {

    isLoggedIn: boolean = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string;

    login(credentials: Object): Observable<boolean> {
        return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
        // this.req.get({
        //     url_id: 'login',
        //     data: userCredentials
        // })
    }

    logout(): Observable<boolean> {
        return Observable.of(true).delay(1000).do(val => this.isLoggedIn = false);
    }

    //===========================================

    isAuth: boolean = false;

    user: UserModel = null;

    constructor() {
    }

    checkpoint() {

    }
}
