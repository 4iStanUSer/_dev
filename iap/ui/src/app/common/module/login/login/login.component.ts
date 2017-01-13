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
        console.log('Data gathered', userCredentials);
        this.auth.login(userCredentials)
            .subscribe(
                () => {
                    if (this.auth.isLoggedIn) {
                        if (this.auth.redirectUrl==null){
                            let redirect = '/landing';
                            console.log("Redirect URL", redirect)
                            this.router.navigate([redirect]);
                        }
                        else{
                            let redirect = this.auth.redirectUrl;
                            console.log("Redirect URL", redirect)
                            this.router.navigate([redirect]);
                        }
                        // Get the redirect URL from our auth service
                        // If no redirect has been set, use the default
                        // let redirect = this.auth.redirectUrl
                        //     ? this.auth.redirectUrl : '/';

                        // Redirect the user
                    }
                },
                (e)=>{
                    console.log("Failed");
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
