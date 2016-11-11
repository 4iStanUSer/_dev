import {Helper} from "./helper";

export interface TimelabelInput {
    full_name: string;
    short_name: string;
    parent_index: number;
    timescale: string;
}

export class TimeLabelModel {
    parent: TimeLabelModel = null;
    children: Array<TimeLabelModel> = [];

    constructor(public full_name: string,
                public short_name: string,
                public timescale: string) {
    }

    addParent(parent: TimeLabelModel) {
        this.removeParent();
        this.parent = parent;
        this.parent.children.push(this);
    }

    removeParent() {
        if (this.parent !== null) {
            let i = 0;
            while (i < this.parent.children.length) {
                if (this.parent.children[i].full_name == this.full_name) {
                    this.parent.children.splice(i, 1);
                } else {
                    i++
                }
            }
            this.parent = null;
        }
    }

    getName(): string {
        return this.full_name;
    }
}

export class TimeLabelsModel {
    private scalesOrder: Array<string> = [];
    storage: Array<TimeLabelModel> = [];
    private pointsByScale: {
        [scale: string]: Array<number>
    } = {};

    constructor(timelabels: Array<TimelabelInput>) {
        let parentsRel = [];
        let scaleRel: { [s: string]: string; } = {};
        // Create Timelabel Objects
        for (let i = 0; i < timelabels.length; i++) {
            this.storage.push(
                new TimeLabelModel(
                    timelabels[i]['full_name'],
                    timelabels[i]['short_name'],
                    timelabels[i]['timescale']
                )
            );
            if (!(timelabels[i]['timescale'] in scaleRel)) {

                if (timelabels[i]['parent_index'] !== null) {
                    scaleRel[timelabels[i]['timescale']] =
                        timelabels[timelabels[i]['parent_index']]['timescale'];
                } else {
                    scaleRel[timelabels[i]['timescale']] = null;
                }
            }
            if (timelabels[i]['parent_index'] !== null
                && timelabels[timelabels[i]['parent_index']]) {
                parentsRel.push({
                    'child': i,
                    'parent': timelabels[i]['parent_index']
                });
            }
            if (!(timelabels[i]['timescale'] in this.pointsByScale)) {
                this.pointsByScale[timelabels[i]['timescale']] = [];
            }
            this.pointsByScale[timelabels[i]['timescale']]
                .push(this.storage.length - 1);
        }
        // Create relations between Timelabel objects
        parentsRel.forEach((el) => {
            try {
                this.storage[el['child']].addParent(this.storage[el['parent']]);
            } catch (e) {
                console.error(e);
            }
        }, this);

        // Note the relations between scales
        let parentTS = Helper.findKey(scaleRel, null);
        if (parentTS) {
            this.scalesOrder.push(parentTS);
            let relLength = Object.keys(scaleRel).length;
            let childTS = null;
            while (relLength != this.scalesOrder.length) {
                childTS = Helper.findKey(scaleRel, parentTS);
                if (childTS) {
                    this.scalesOrder.push(childTS);
                    parentTS = childTS;
                } else {
                    console.error('Something wrong: have no such value');
                    break;
                }
            }
        }
    }

    getScales() {
        return this.scalesOrder;
    }

    getScaleTimelabels(scale: string): Array<TimeLabelModel> {
        if (this.pointsByScale[scale]) {
            return this.pointsByScale[scale].map((el)=> {
                return this.storage[el];
            }, this);
        }
        return [];
    }

    getTimeLabel(scale: string, full_name: string): TimeLabelModel {
        for (let i=0;i<this.storage.length;i++) {
            if (this.storage[i]['full_name'] == full_name
                && this.storage[i]['timescale'] == scale) {
                return this.storage[i];
            }
        }
        return null;
    }
}
