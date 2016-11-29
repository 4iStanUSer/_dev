import {Injectable} from '@angular/core';
import {AjaxService} from "./../../common/service/ajax.service";
import {StaticDataService} from "../../common/service/static-data.service";
import { ProjectInfo, UserAction } from './landing-page.model'


import { PROJECTINFO, USERACTIONS, LABELS} from './landing.mock'
import {Subject} from 'rxjs/Subject';

@Injectable()
export class LandingPageService {

    private pageName: string = 'forecast-landing';
    projectInfo: ProjectInfo = null;

    constructor(
        private req: AjaxService,
        private sds: StaticDataService
    ) {}

    getConfig(): Subject<Object> {
        let subject = new Subject();
        subject.subscribe();
        setTimeout(() => {subject.next(LABELS)}, 10);
        return subject;
    }

    getProjectInfo(): Subject<ProjectInfo> {
        if (this.projectInfo) {
            let subject = new Subject();
            subject.subscribe(() => {
                return this.projectInfo;
            });
            setTimeout(() => {subject.next()}, 10);
            return subject;
        }
        else {
            let subject = new Subject();
            subject.subscribe((d) => {
                this.projectInfo = <ProjectInfo>d;
                return this.projectInfo;
            });
            setTimeout(() => {subject.next(PROJECTINFO)}, 10);
            return subject;
            //this.req.get({
            //    'url_id': 'common/get_project_info',
            //}).subscribe((d)=> {
            //        this.projectInfo = <ProjectInfo>d
            //        return this.projectInfo
            //    },
            //    (e)=> {
            //        return this.projectInfo
            //    });
        }

    }

    getRecentActions(): Subject<UserAction[]> {
        let subject = new Subject();
        subject.subscribe((d) => {
            return USERACTIONS;
        });
        setTimeout(() => {subject.next(USERACTIONS)}, 10);
        return subject;

        //return this.req.get({'url_id': 'forecast/get_recent_actions'})
        //    .subscribe((d)=> {return d}, (e)=> {return []});
    }
}
