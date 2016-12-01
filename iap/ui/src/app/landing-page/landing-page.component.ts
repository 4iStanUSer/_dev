import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

import {AjaxService} from "../common/service/ajax.service";
import {AuthService} from "../common/service/auth.service";



@Component({
    templateUrl: './landing-page.component.html',
    styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {

    constructor(private router: Router, private req: AjaxService, private auth: AuthService) {
    }

    ngOnInit() {

    }

    onClickLogout() {
        this.auth.logout()
            .subscribe(
                () => {
                    this.router.navigate(['/']);
                },
                (e) => {
                    console.log(e);
                },
                () => {
                    console.log('Complete!');
                }
            );
    }

}
