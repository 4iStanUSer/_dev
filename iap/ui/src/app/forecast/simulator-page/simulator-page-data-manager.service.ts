import {Injectable} from '@angular/core';

import {AjaxService} from "./../../common/service/ajax.service";

@Injectable()
export class SimulatorPageDataManagerService {

    private scales: Array<string> = [];
    private timelabels = [];

    private variables = {};
    private data = {};
    private cagrs = {};

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
            this.variables = d['variables'];
            this.data = d['data'];
            this.cagrs = d['cagrs'];
        });
        return resp;
    }

    public getData_VTable() {
        return {
            'variables': this.variables,
            'data': this.data,
            'timelabels': this.timelabels,
            'scales_order': this.scales, // ['annual', 'quarterly', 'monthly']
            'config': {
                'head': {
                    'horizontal_order': ['sales', 'volume', 'price'],
                    'vertical_order': [
                        {
                            'key': 'name',
                            'label': 'Name'
                        },
                        {
                            'key': 'metric',
                            'label': 'Metric'
                        }
                    ]
                }
            }
        };
    }

    // TODO Move recreateScales() & _findKey() to common part or into Table model (VL)
    private recreateScales(): void {
        this.scales = [];

        let pIndex: number = null;
        let ts: string = null;
        let relations: { [s: string]: string; } = {}; // {child: parent}

        for (let i = 0; i < this.timelabels.length; i++) {
            pIndex = this.timelabels[i]['parent_index'];
            ts = this.timelabels[i]['timescale'];

            if (!('children' in this.timelabels[i])) {
                this.timelabels[i]['children'] = [];
            }

            if (pIndex !== null) {
                if (!this.timelabels[pIndex]) {
                    console.error('Not found such index ' + pIndex);
                    break;
                }
                if (!('children' in this.timelabels[pIndex])) {
                    this.timelabels[pIndex]['children'] = [];
                }
                this.timelabels[pIndex]['children'].push(i);
            }
            if (!(ts in relations)) {
                if (pIndex !== null) {
                    relations[ts] = this.timelabels[pIndex]['timescale'];
                } else {
                    relations[ts] = null;
                }
            }
        }

        let parentTS = this._findKey(relations, null);
        if (parentTS) {
            this.scales.push(parentTS);
            let relLength = Object.keys(relations).length;
            let childTS = null;
            while (relLength != this.scales.length) {
                childTS = this._findKey(relations, parentTS);
                if (childTS) {
                    this.scales.push(childTS);
                    parentTS = childTS;
                } else {
                    console.error('Something wrong: have no such value');
                    break;
                }
            }
        }
    }

    public _findKey(obj: Object, value: any): string {
        for (var prop in obj) {
            if (obj.hasOwnProperty(prop)) {
                if (obj[prop] === value)
                    return prop;
            }
        }
    }
}
