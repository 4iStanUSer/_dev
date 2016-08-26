import { Component, OnInit, Input } from '@angular/core';
import { RangeSliderComponent, RangeSliderChange } from './../range-slider/';

@Component({
    // moduleId: module.id,
    selector: 'period-selector',
    directives: [RangeSliderComponent],
    template: `
    <div class="row">
        <div class="form-group col-sm-6">
            <label class="">Start point:</label>
            <select 
                class="form-control" 
                placeholder="Start point"
                (ngModelChange)="changePoint('start', $event)"
                [(ngModel)]="startPoint"
                >
                <option *ngFor="let opt of availableForStart" [value]="opt" [attr.selected]="opt==startPoint">
                    {{ opt }}
                </option>
            </select>
        </div>
        <div class="form-group col-sm-6">
            <label class="">End point:</label>
            <select 
                class="form-control" 
                placeholder="End point"
                (ngModelChange)="changePoint('end', $event)"
                [(ngModel)]="endPoint">
                <option *ngFor="let opt of availableForEnd" [value]="opt" [attr.selected]="opt==endPoint">
                    {{ opt }}
                </option>
            </select>
        </div>
    </div>

    <div class="row">
        <range-slider [minimal-period-length]="minimalPeriod" [range-list]="range" [start-point]="startPoint" [end-point]="endPoint" (slide)="onSlide($event)"></range-slider>
    </div>
    `
})
export class PeriodSelectorComponent implements OnInit {
    @Input('start-point') startPoint: string;
    @Input('end-point') endPoint: string;
    @Input('range-list') range: string[];
    @Input('minimal-period-length') minimalPeriod: number;

    private availableForStart: string[] = [];
    private availableForEnd: string[] = [];

    onSlide(changes: RangeSliderChange) {
        if (changes && changes.point && changes.newValue) {
            this.changePoint(changes.point, changes.newValue);
        }
        return false;
    }

    constructor() { }

    ngOnInit() {
        this.availableForStart = this.range.slice(0, this.range.length - this.minimalPeriod);
        this.availableForEnd = this.range.slice(this.minimalPeriod);
        //this.changePoint();
    }

    changePoint(point?: string, newValue?: string) {
        console.log('changePoint');

        var sp = (point == 'start') ? newValue : this.startPoint;
        var ep = (point == 'end') ? newValue : this.endPoint;

        var indS = this.availableForStart.indexOf(sp);
        var indE = this.availableForEnd.indexOf(ep);

        if (point == 'end') {
            if (indE === -1) {
                if (this.endPoint) {
                    this.endPoint = this.endPoint;
                } else {
                    this.endPoint = this.availableForEnd[this.availableForEnd.length - 1];
                }
            } else {
                indS = this.range.indexOf(sp);
                indE = this.range.indexOf(ep);
                if (this.minimalPeriod > indE - indS) {
                    this.startPoint = this.range[indE - this.minimalPeriod];
                }
                this.endPoint = ep;
            }
        } else {
            if (indS === -1) {
                if (this.startPoint) {
                    this.startPoint = this.startPoint;
                } else {
                    this.startPoint = this.availableForStart[0];
                }
            } else {
                indS = this.range.indexOf(sp);
                indE = this.range.indexOf(ep);
                if (this.minimalPeriod > indE - indS) {
                    this.endPoint = this.range[indS + this.minimalPeriod];
                }
                this.startPoint = sp;
            }
        }
    }
}

