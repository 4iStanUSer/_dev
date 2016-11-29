import { Component, OnInit } from '@angular/core';
import { ProjectInfo, UserAction } from './landing-page.model'
import { LandingPageService } from './landing-page.service'

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {

    labels: Object;
    projectInfo: ProjectInfo;
    recentActions: UserAction[];

    constructor(
        private pageManager: LandingPageService
    ) { }

    ngOnInit() {
        this.pageManager.getConfig().subscribe((d) => {this.labels = d});
        this.pageManager.getProjectInfo()
            .subscribe((d) => {this.projectInfo = d;});
        this.pageManager.getRecentActions()
            .subscribe((d) => {this.recentActions = d});
    }
}

