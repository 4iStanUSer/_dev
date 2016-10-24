import {Injectable} from '@angular/core';

import {AjaxService} from "./../../common/service/ajax.service";
import {TableModel} from "../../common/model/table.model";

@Injectable()
export class SimulatorPageDataManagerService {

    private scales: Array<string> = [];
    private timelabels = [];
    private variables = {};
    private data = {};
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
            //this.variables = d['variables'];

            for (let i = 0; i < d['variables'].length; i++) { // TODO Remove
                this.variables[d['variables'][i]['name']] = d['variables'][i];
            }

            let tableModel = new TableModel(this.variables, this.timelabels, this.data);
            console.log(tableModel);

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

            this.recreateScales();
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
                    'horizontal_order': Object.keys(this.variables), //['sales', 'volume', 'price'],
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
