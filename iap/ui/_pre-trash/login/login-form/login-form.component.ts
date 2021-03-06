import { Component, OnInit } from '@angular/core';
import {AlertService} from "../services/alert.service";
import {AjaxService} from "../../../service/ajax.service";

@Component({
    selector: 'login-form',
    templateUrl: 'login-form.component.html',
    styleUrls: ['login-form.component.css']
})

export class LoginFormComponent implements OnInit {
    model: any = {};

    constructor(
        private req: AjaxService,
        private alertService: AlertService) { }

    ngOnInit() {
    }

    login() {
        let userCredentials = {
            username: this.model.username,
            password: this.model.password
        }
        this.req.post({
            url_id: 'login',
            data: userCredentials
        }).subscribe(
            () => {
                console.log(userCredentials)
                console.log('Successful login');
            },
            (e) => {
                console.log("")
                console.log(e);
                this.alertService.error(e);
            },
            () => {
                console.log(userCredentials)
                console.log('Complete!');
            }
        );
    }
}

