import { Component }        from '@angular/core';
import { Router} from '@angular/router';
import { AuthService } from "./auth.service"

@Component({
    templateUrl: 'page/login.component.html',
    styleUrls: ['page/login.component.css']
})

export class LoginPageComponent {

    message: string;
    model: any = {};

  constructor(public router: Router, public  auth: AuthService) {
  }

  login() {
        let username = this.model.username;
        let password = this.model.password;
        this.message = 'Trying to log in ...';
        console.log(username, password);
        this.auth.login(username, password);

   }

  logout()
        {
        console.log("logout");
        this.auth.logout();
        }
    }
