import {Component} from "@angular/core"
import { NotificationService }     from '../service/notification.service';

@Component({
    templateUrl: 'test.html',
    selector: 'test',
    providers: [NotificationService]
})

export class TestComponent{

    constructor(private missionService: NotificationService) {

        missionService.getResponse().subscribe(
            button=>{console.log(button)

            }
        )
    }

    announce() {

        let config = {
                    'header':"Modal Header",
                    'body': "Text of body",
                    'buttons': ['Ok', 'Cancel', 'Skip'],
                    'style': {'color':'red', 'background-color':'red'},
                    'type':'warning'
                    }

        return this.missionService.setHeader(config);

      }

    announce_1() {

        let config = {
                    'header':"Modal Header",
                    'body': "This is information windows \n that...",
                    'buttons': ['No', 'Cancel', 'Skip'],
                    'style': {'color':'red', 'background-color':'red'},
                    'type':'info'
                    }

        return this.missionService.setHeader(config);

      }

}
