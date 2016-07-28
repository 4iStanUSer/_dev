import { Injectable } from '@angular/core';
import { AjaxService } from "./../../common/service/request.service";

@Injectable()
export class IndexPageService {

    constructor(private req: AjaxService) { }

    public get_dimension(dimension_name: string) {

        return this.req.get({
            url: '/forecast/get_dimension_selector',
            data: {
                dimension: dimension_name,
                asd: {
                    asd1: 123,
                    asd2: [1, 2, 'rty']
                },
                qwe: [
                    1, 2, 'rty'
                ]
            }
        });
    }

    public get_time_series() {
        return this.req.get({
            url: '/forecast/get_time_series',
            data: { }
        });
    }


}
