import { Component }        from '@angular/core';
import { Router} from '@angular/router';
import { AuthService } from "../auth.service"

@Component({
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css']
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
        this.auth.login(username, password);

   }

  logout()
        {
        this.auth.logout();
        }
    }
