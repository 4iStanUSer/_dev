import {Component, OnInit} from '@angular/core';
import {DataManagerService} from './data-manager.service';

@Component({
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    constructor(private dm: DataManagerService) {
    }

    ngOnInit() {
        this.dm.init()
            .subscribe((a) => {
                console.log('DashboardComponent->subscribe');
            });
    }
}
