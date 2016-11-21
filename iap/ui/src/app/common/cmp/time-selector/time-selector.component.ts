import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges,
    Input,
    Output,
    EventEmitter
} from '@angular/core';


export interface TimeSelectorDataInput {
    order: Array<string>;
    timescales: {
        [timescale: string]: Array<{
            full_name: string;
            short_name: string;
            timescale: string;
        }>;
    }
}
export interface TimeSelectorSelectedData {
    start: string;
    end: string;
    scale: string;
    mid?: string;
}

export class Sliders {
    start: PointModel;
    end: PointModel;
    mid?: PointModel;
}


class ScalesModel {
    order: Array<string> = [];
    pointsByScale: {
        [scale: string]: Array<PointModel>
    } = null;

    constructor(order: Array<string>,
                timescales: {
                    [scale: string]: Array<{
                        full_name: string;
                        short_name: string;
                        timescale: string;
                    }>
                }) {

        let l = order.length;
        this.pointsByScale = {};
        for (let i = 0; i < l; i++) {
            if (timescales[order[i]] && timescales[order[i]].length) {
                this.order.push(order[i]);
                for (let j = 0; j < timescales[order[i]].length; j++) {
                    let tl = timescales[order[i]][j];
                    let point = new PointModel(
                        tl.full_name, tl.full_name,
                        tl.short_name, tl.timescale);
                    if (!this.pointsByScale[order[i]]) {
                        this.pointsByScale[order[i]] = [];
                    }
                    this.pointsByScale[order[i]].push(point);
                }
            }
        }
    }

    getScales(): Array<string> {
        return this.order;
    }

    getPoint(scale: string, name: string): PointModel {
        if (this.pointsByScale[scale]) {
            let l = this.pointsByScale[scale].length;
            for (let i = 0; i < l; i++) {
                if (this.pointsByScale[scale][i]['full_name'] == name) {
                    return this.pointsByScale[scale][i];
                }
            }
        }
        return null;
    }

    getPointsForScale(scale: string): Array<PointModel> {
        return (this.pointsByScale[scale]) ? this.pointsByScale[scale] : [];
    }
}

class PointModel {
    constructor(public id: string,
                public full_name: string,
                public short_name: string,
                public scale: string) {
    }

    getName(): string {
        return this.full_name;
    }
}


@Component({
    selector: 'time-selector',
    templateUrl: './time-selector.component.html',
    styleUrls: ['./time-selector.component.css']
})
export class TimeSelectorComponent implements OnInit, OnChanges {

    private lang = {
        'apply': 'Apply',
        'cancel': 'Cancel'
    };

    private scalesM: ScalesModel = null;

    /*--Vars for view--*/
    private scales: Array<string> = [];
    private currScale: string = null;
    private currPoints: Array<PointModel> = [];
    private expandedMode: boolean = false;

    private selectedPoints: Sliders = new Sliders();
    private preSelectedPoints: {
        [timescale: string]: Sliders
    } = null;


    constructor() {
    }

    ngOnInit() {
    }

    @Input() data: TimeSelectorDataInput = null;
    @Input() selected: TimeSelectorSelectedData = null;


    @Output() changed = new EventEmitter(); //: EventEmitter<TimePeriodInput>

    ngOnChanges(ch: SimpleChanges) {
        console.info('TimeSelectorComponent: ngOnChanges()');
        if (ch['data']) {

            let d = ch['data']['currentValue'];
            this.scalesM = new ScalesModel(d['order'], d['timescales']);
            this.scales = this.scalesM.getScales();

            if (this.scales.length) {
                this.preSelectedPoints = {};
                for (let i = 0; i < this.scales.length; i++) {
                    this.preSelectedPoints[this.scales[i]] = new Sliders();
                }
            }
        }
        if (ch['selected']) {
            let selScale = null;
            let scale = ch['selected']['currentValue']['scale'];
            for (let prop in ch['selected']['currentValue']) {
                if (prop == 'scale') continue;

                try {

                    let pointName = ch['selected']['currentValue'][prop];
                    let t = this.scalesM.getPoint(scale, pointName);

                    if (t) {
                        if (selScale === null) {
                            selScale = t.scale;
                        }
                        if (t.scale == selScale) {
                            this.selectedPoints[prop] = t;
                            this.preSelectedPoints[selScale][prop] = t;
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
            this.currPoints = this.scalesM.getPointsForScale(scale);

            if (!this.preSelectedPoints[scale]['start']) {
                this.preSelectedPoints[scale]['start'] = this.currPoints[0];
            }
            if (!this.preSelectedPoints[scale]['end']) {
                this.preSelectedPoints[scale]['end'] =
                    this.currPoints[this.currPoints.length - 1];
            }
        }
    }

    private setExpandedMode(mode: boolean) {
        this.expandedMode = !!mode;
    }

    private onSliderChange(ch) {
        try {
            this.preSelectedPoints[this.currScale][ch['slider']] = ch['value'];
        } catch (e) {
            console.error(e);
        }
    }

    private save() {
        this.selectedPoints['start'] = this.preSelectedPoints[this.currScale]['start'];
        this.selectedPoints['end'] = this.preSelectedPoints[this.currScale]['end'];
        this.selectedPoints['mid'] = this.preSelectedPoints[this.currScale]['mid'];

        this.setExpandedMode(false);

        this.changed.emit({
            'scale': this.currScale,
            'start': this.selectedPoints['start']['full_name'],
            'end': this.selectedPoints['end']['full_name'],
            'mid': ((this.selectedPoints['mid']
            && this.selectedPoints['mid']['full_name'])
                ? this.selectedPoints['mid']['full_name'] : null)
        });
    }
}
