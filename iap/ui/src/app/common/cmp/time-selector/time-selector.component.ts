import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges,
    Input,
    Output,
    EventEmitter
} from '@angular/core';

import {
    TimelabelInput,
    TimeLabelModel,
    TimeLabelsModel
} from "../../model/time-labels.model";
import {TimePeriodInput} from "../../model/time-period.model";


export class Sliders {
    start: TimeLabelModel;
    end: TimeLabelModel;
    // mid: TimeLabel;
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

    private timelabels: TimeLabelsModel = null;

    /*--Vars for view--*/
    private scales: Array<string> = [];
    private currScale: string = null;
    private currPoints: Array<TimeLabelModel> = [];
    private expandedMode: boolean = false;

    private selectedPoints: Sliders = new Sliders();
    private preSelectedPoints: {
        [timescale: string]: Sliders
    } = null;


    constructor() {
    }

    ngOnInit() {
    }

    @Input() data: Array<TimelabelInput> = [];
    @Input() selected: TimePeriodInput = null;
    // {
    //     start: {scale: string, full_name: string},
    //     end: {scale: string, full_name: string},
    //     mid?: {scale: string, full_name: string},
    // };

    @Output() changed = new EventEmitter(); //: EventEmitter<TimePeriodInput>
    // {
    //     start: {scale: string, full_name: string},
    //     end: {scale: string, full_name: string},
    //     mid?: {scale: string, full_name: string},
    // }

    ngOnChanges(ch: SimpleChanges) {
        console.info('TimeSelectorComponent: ngOnChanges()');
        if (ch['data']) {
            this.timelabels = new TimeLabelsModel(ch['data']['currentValue']);
            this.scales = this.timelabels.getScales();
            if (this.scales.length) {
                this.preSelectedPoints = {};
                for (let i = 0;i<this.scales.length;i++) {
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
                    let timelabel = ch['selected']['currentValue'][prop];
                    // let scale = timelabel['scale'];
                    // let full_name = timelabel; //['full_name'];
                    let t = this.timelabels.getTimeLabel(scale, timelabel);

                    if (t) {
                        if (selScale === null) {
                            selScale = t.timescale;
                        }
                        if (t.timescale == selScale) {
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
            this.currPoints = this.timelabels.getScaleTimelabels(scale);

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
        // this.selectedPoints[this.currScale]['mid'] = this.preSelectedPoints['mid'];

        this.setExpandedMode(false);
        // TODO Emit event
        this.changed.emit({
            'scale': this.currScale,
            'start': this.selectedPoints['start']['full_name'],
            'end': this.selectedPoints['end']['full_name'],
        });
    }
}
