import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from "../../../service/auth.service";

@Component({
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
/**
 * Simple component to show login form and catch some events on it
 */
export class LoginComponent implements OnInit {
    model: any = {};

    constructor(public auth: AuthService, public router: Router) {
    }

    ngOnInit() {
    }

    login() {
        let userCredentials = {
            username: this.model.username,
            password: this.model.password
        };
        this.auth.login(userCredentials)
            .subscribe(
                () => {
                    if (this.auth.isLoggedIn) {
                        // Get the redirect URL from our auth service
                        // If no redirect has been set, use the default
                        // let redirect = this.auth.redirectUrl
                        //     ? this.auth.redirectUrl : '/';
                        let redirect = '/forecast'; // TODO Review ability to get this from outside
                        // Redirect the user
                        this.router.navigate([redirect]);
                    }
                },
                (e) => {
                    console.log(e);
                },
                () => {
                    console.log('Complete!');
                }
            );
    }

    logout() {
        this.auth.logout();
    }

}
