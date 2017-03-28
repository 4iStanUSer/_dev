import { Component, Input, OnDestroy } from '@angular/core';
import { NotificationService } from './notification.service';
import { Subscription }   from 'rxjs/Subscription';

@Component({
  selector: 'notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.style.css']
})

export class NotificationComponent implements OnDestroy{

    @Input()
    header:string;
    body:string;
    buttons:any[];
    subscription: Subscription;
    type:string = "default";
    style:any;

    constructor(private notificationService: NotificationService){

        this.subscription = this.notificationService.getMessage().subscribe(
        config => {
                   this.header = config['header'];
                   this.body = config['body'];
                   this.buttons = config['buttons'];

                   if (config['type']){

                       this.type = config['type'];
                   }

                   else if (config['style']){

                       this.style = config['style'];
                       console.log(this.style);
                   }


            }
        );


    };

    callBack(button){
        this.notificationService.setResponse(button);
    }


    ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
