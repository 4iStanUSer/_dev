import { Component, Input, OnDestroy } from '@angular/core';
import { NotificationService } from '../service/notification.service';
import { Subscription }   from 'rxjs/Subscription';

@Component({
  selector: 'notification',
  templateUrl: 'notification.component.html',
  styleUrls: ['notification.style.css']
})

export class NotificationComponent implements OnDestroy{

    @Input()
    header:string;
    body:string;
    buttons:any[];
    subscription: Subscription;
    type:string = "notrealised";
    style:any;

    constructor(private notificationService: NotificationService){

        this.subscription = this.notificationService.getMessage().subscribe(
        config => {
                   console.log("Config Received");
                   this.header = config['header'];
                   this.body = config['body'];
                   this.buttons = config['buttons'];

                   if (config['type']){

                       this.type = config['type'];
                   }

                   else if (config['style']){

                       this.style = config['style'];
                       this.style = "default";
                   }


            }
        );


    };

    callBack(button) {
        console.log(button);
        if (button == "Skip"){
            this.type="notrealised";
           }
        else {
            console.log(button);
            this.notificationService.setResponse(button);

        }
    }

    ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
