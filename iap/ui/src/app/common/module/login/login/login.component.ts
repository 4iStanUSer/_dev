import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from "../../../service/auth.service";

@Component({
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
    model: any = {};
    message: string;

    constructor(public auth: AuthService, public router: Router) {
        this.setMessage();
    }

    ngOnInit() {
    }

    setMessage() {
        this.message = 'Logged ' + (this.auth.isLoggedIn ? 'in' : 'out');
    }

    login() {
        this.message = 'Trying to log in ...';
        let userCredentials = {
            username: this.model.username,
            password: this.model.password
        };
        this.auth.login(userCredentials)
            .subscribe(
                () => {
                    this.setMessage();
                    if (this.auth.isLoggedIn) {
                        // Get the redirect URL from our auth service
                        // If no redirect has been set, use the default
                        // let redirect = this.auth.redirectUrl
                        //     ? this.auth.redirectUrl : '/';
                        let redirect = '/forecast';
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
        this.setMessage();
    }

}
