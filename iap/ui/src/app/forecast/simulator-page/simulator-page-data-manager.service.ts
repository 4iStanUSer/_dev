import {Injectable} from '@angular/core';

import {AjaxService} from "./../../common/service/ajax.service";

@Injectable()
export class SimulatorPageDataManagerService {

    private timelabels = [];
    private variables = {};
    public data = {};
    private cagrs = {};

    private cagrPeriods: Array<{start: string, end: string}> = [];
    private timelabelsMap: {[timeLabel: string]: number} = {};

    constructor(private req: AjaxService) {
    }


    init(id?: number|string) {
        let data = {};
        if (id && +id) {
            data['entity_id'] = +id;
        }
        let resp = this.req.get({
            'url': '/forecast/get_dashboard_data',
            'data': data
        });

        resp.subscribe((d)=>{

            this.timelabels = d['timelabels'];
            this.data = d['data'];
            this.cagrs = d['cagrs'];
            this.variables = d['variables'];

            // for filling cagr periods
            let cKeys: Array<string> = Object.keys(this.cagrs);
            if (cKeys.length) {
                for (let i = 0; i < this.cagrs[cKeys[0]].length; i++) {
                    let cagr = this.cagrs[cKeys[0]][i];
                    let exist = false;
                    for (let j = 0; j < this.cagrPeriods.length; j++) {
                        if (this.cagrPeriods[j]['start']
                            == cagr['start'].toString()
                            && this.cagrPeriods[j]['end']
                            == cagr['end'].toString()) {
                            exist = true;
                            break;
                        }
                    }
                    if (!exist) {
                        this.cagrPeriods.push({
                            'start': cagr['start'].toString(),
                            'end': cagr['end'].toString()
                        });
                    }
                }
            }

            // Fill timelabelsMap -> {timeLabel: timelabelIndex}
            for (let i = 0; i < this.timelabels.length; i++) {
                this.timelabelsMap[this.timelabels[i]['name']] = i;
            }

        });
        return resp;
    }

    public getData_VTable() {

        return {
            'variables': this.variables,
            'timelabels': this.timelabels,
            'data': this.data,

            // 'scales_order': this.scales, // ['annual', 'quarterly', 'monthly']
            // 'config': {
            //     'head': {
            //         'horizontal_order': Object.keys(this.variables), //['sales', 'volume', 'price'],
            //         'vertical_order': [
            //             {
            //                 'key': 'name',
            //                 'label': 'Name'
            //             },
            //             {
            //                 'key': 'metric',
            //                 'label': 'Metric'
            //             }
            //         ]
            //     }
            // }
        };
    }

}
