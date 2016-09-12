import { Component, OnInit } from '@angular/core';
import {LoginService} from "../../service/login.service";
import {User} from "./user";

@Component({
  selector: 'app-login-widget',
  templateUrl: 'login-widget.component.html',
  styleUrls: ['login-widget.component.css']
})
export class LoginWidgetComponent implements OnInit {
    constructor(private loginService: LoginService) { }

    model = new User(0, '', '');
    submitted = false;

    users: User[]; //tmp

    onSubmit() { this.submitted = true; }

    validationErrorMessage(input_type: string): string {
        if (input_type == 'email') {
            let x = this.model.email;
            let atpos = x.indexOf("@");
            let dotpos = x.lastIndexOf(".");
            if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= x.length) {
                return 'Not a valid e-mail address';
            }
            else {
                return '';
            }
        }
        if (input_type == 'password') {
            let x = this.model.password;
            if (x.length <= 6) {
                return 'Too short password (at least 6 symbols needed)';
            }
            else {
                return '';
            }
        }
    }

    getUsers(): void {
        //this.users = this.loginService.getUsers();
        this.loginService.getUsers().subscribe(users => this.users = users)
        // this.loginService.getUsers().then(users => this.users = users);
        //this.heroService.getHeroes().then(heroes => this.heroes = heroes);
    }

    ngOnInit() {
        this.getUsers();
    }

    login(): void {
        let data = [this.model.email, this.model.password]
        this.loginService.doLogin(data)
    }

    // TODO: Rewrite this
    get diagnostic() { return JSON.stringify(this.model); }

    showFormControls(form: any) {
        return form && form.controls['email'] &&
            form.controls['email'].value; //
    }

}
