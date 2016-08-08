import { Injectable } from '@angular/core';
import { AjaxService } from "./../../common/service/ajax.service";

@Injectable()
export class IndexPageService {

    constructor(private req: AjaxService) { }

    public get_index_page_data(selection){
        return this.req.get({
            url: '/forecast/get_index_page_data',
            data: selection
        });
    }
}
