import {Component} from "@angular/core"
import { NotificationService }     from '../service/notification.service';
import {AuthService} from "../login-page/auth.service";

@Component({
    templateUrl: 'user_menu.html',
    selector: 'user_menu',
    providers: [NotificationService]
})

export class UserMenu{

    constructor(private notificationService: NotificationService, private auth: AuthService) {

        notificationService.getResponse().subscribe(
            button=>{console.log(button)

            }
        )
    }

    announce() {

        console.log("Start Notification");

        let config = {
                    'header':"Modal Header",
                    'body': "Text of body",
                    'buttons': ['Ok', 'Cancel', 'Skip'],
                    'style': {'color':'red', 'background-color':'red'},
                    'type':'warning'
                    }

        return this.notificationService.setHeader(config);

      }


}
