import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges,
    Input
} from '@angular/core';
import {Helper} from './../../model/helper';
import {RangeSliderComponent} from "./range-slider/range-slider.component";

interface TimelabelInput {
    full_name: string;
    short_name: string;
    parent_index: number;
    timescale: string;
}
export class Sliders {
    start: TimeLabel;
    end: TimeLabel;
    // mid: TimeLabel;
}

export class TimeLabel {
    parent: TimeLabel = null;
    children: Array<TimeLabel> = [];

    constructor(public full_name: string,
                public short_name: string,
                public timescale: string) {
    }

    addParent(parent: TimeLabel) {
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

    getName() {
        return this.full_name;
    }
}

class TimeLabels {
    private scalesOrder: Array<string> = [];
    private storage: Array<TimeLabel> = [];
    private pointsByScale: {
        [scale: string]: Array<number>
    } = {};

    constructor(timelabels: Array<TimelabelInput>) {
        let parentsRel = [];
        let scaleRel: { [s: string]: string; } = {};
        // Create Timelabel Objects
        for (let i = 0; i < timelabels.length; i++) {
            this.storage.push(
                new TimeLabel(
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

    getScaleTimelabels(scale: string): Array<TimeLabel> {
        if (this.pointsByScale[scale]) {
            return this.pointsByScale[scale].map((el)=> {
                return this.storage[el];
            }, this);
        }
        return [];
    }

    getTimeLabel(scale: string, full_name: string): TimeLabel {
        for (let i=0;i<this.storage.length;i++) {
            if (this.storage[i]['full_name'] == full_name
                && this.storage[i]['scale'] == scale) {
                return this.storage[i];
            }
        }
        return null;
    }
}


@Component({
    selector: 'time-selector',
    providers: [RangeSliderComponent],
    templateUrl: './time-selector.component.html',
    styleUrls: ['./time-selector.component.css']
})
export class TimeSelectorComponent implements OnInit, OnChanges {

    // private slider: SliderRenderer = null;
    private lang = {
        'apply': 'Apply',
        'cancel': 'Cancel'
    };

    private timelabels: TimeLabels = null;

    /*--Vars for view--*/
    private scales: Array<string> = [];
    private currScale: string = null;
    private currPoints: Array<TimeLabel> = [];
    private expandedMode: boolean = false;
    private selectedPoints: {
        [timescale: string]: Sliders // TODO Save state of preSelected!!!
    } = null;
    private preSelectedPoints: Sliders = new Sliders(); //{start: null, end: null};


    // @Input() set data(d: Array<TimelabelInput>) {
    //     console.info('TimeSelectorComponent: set data');
    //     this.timelabels = new TimeLabels(d);
    //     this.scales = this.timelabels.getScales();
    //     if (this.scales.length) {
    //         this.changeScale(this.scales[0]);
    //     }
    // }


    constructor() {
    }

    ngOnInit() {
    }

    @Input() data: Array<TimelabelInput> = [];
    @Input() selected: {
        start: {scale: string, full_name: string},
        end: {scale: string, full_name: string},
        mid?: {scale: string, full_name: string},
    };

    ngOnChanges(ch: SimpleChanges) {
        console.info('TimeSelectorComponent: ngOnChanges()');
        if (ch['data']) {
            this.timelabels = new TimeLabels(ch['data']['currentValue']);
            this.scales = this.timelabels.getScales();
            if (this.scales.length) {
                this.selectedPoints = {};
                for (let i = 0;i<this.scales.length;i++) {
                    this.selectedPoints[this.scales[i]] = new Sliders();
                    // {
                    //     start: null, end: null, mid: null
                    // };
                }
                // this.selectedPoints = sel;
                //this.changeScale(this.scales[0]);
            }
        }
        if (ch['selected']) {
            // {scale: string, full_name: string}
            let selScale = null;
            for (let prop in ch['selected']['currentValue']) {
                try {
                    let timelabel = ch['selected']['currentValue'][prop];
                    let scale = timelabel['scale'];
                    let full_name = timelabel['full_name'];
                    let t = this.timelabels.getTimeLabel(scale, full_name);
                    if (t) {
                        if (selScale === null) {
                            selScale = t.timescale;
                        }
                        if (t.timescale == selScale) {
                            this.selectedPoints[selScale][prop] = t;
                        } else {
                            if (prop == 'start') {

                            } else if (prop == 'end') {

                            } else {
                                // TODO
                            }
                        }
                    }
                } catch (e) {
                    console.error(e);
                }
            }
            this.currScale = (selScale) ? selScale : null;
        }
        if (this.scales.length) {
            if (!this.currScale) {
                this.currScale = this.scales[0];
            }
            this.changeScale(this.currScale);
        }
    }


    private changeScale(scale: string) {
        if (this.scales.indexOf(scale) !== -1) {
            this.currScale = scale;
            this.currPoints = this.timelabels.getScaleTimelabels(scale);
            // TODO get preSelectedPoints from selected
            this.preSelectedPoints = {
                'start': (this.currPoints[0]) ? this.currPoints[0] : null,
                'end': (this.currPoints[this.currPoints.length - 1])
                    ? this.currPoints[this.currPoints.length - 1] : null,
                //'mid': null,
            };


            // And others actions - UPDATE SLIDER ...
        }
    }

    private setExpandedMode(mode: boolean) {
        this.expandedMode = !!mode;
    }

    private onSliderChange(ch) {
        try {
            this.preSelectedPoints[ch['slider']] = ch['value'];
        } catch (e) {
            console.error(e);
        }
    }

    private save() {
        console.log('save');
        this.selectedPoints[this.currScale]['start'] = this.preSelectedPoints['start'];
        this.selectedPoints[this.currScale]['end'] = this.preSelectedPoints['end'];
        this.selectedPoints[this.currScale]['mid'] = this.preSelectedPoints['mid'];
        this.setExpandedMode(false);
        // TODO Change visible selection
        // TODO Emit event
    }
}
