/**
 * Created by Alex on 24.03.2017.
 */
import {Component} from "@angular/core"
import { NotificationService }     from './notification.service';


@Component({
    templateUrl: 'test.html',
    selector: 'test',
    providers: [NotificationService]
})

export class TestComponent{

    constructor(private missionService: NotificationService) {

        missionService.getResponse().subscribe(
            button=>{console.log(button)}
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

}
