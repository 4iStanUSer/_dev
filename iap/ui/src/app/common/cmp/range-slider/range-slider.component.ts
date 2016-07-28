import {Component, ElementRef, OnInit, Input, Output,
    EventEmitter} from '@angular/core';

declare var jQuery: any;
declare var noUiSlider: any;

export class RangeSliderChange {
    public point: string;
    public newValue: string;
}

@Component({
    moduleId: module.id,
    selector: 'range-slider',
    template: `<div class="rangeSlider"></div>`,
    styles: [`
        .noUi-horizontal .noUi-handle-lower .noUi-tooltip {
            display:none!important;
        }
        .noUi-horizontal .noUi-handle-lower :active .noUi-tooltip {
            display:block!important;
        }
    `]
})
export class RangeSliderComponent implements OnInit {
    private slider: any;

    @Input('range-list') range: string[];
    @Input('minimal-period-length') minimalPeriod: number;

    @Output() slide = new EventEmitter<RangeSliderChange>();


    _startPoint: string;
    _endPoint: string;

    @Input('start-point')
    set startPoint(value: string) {
        if (this.slider) {
            this.slider.noUiSlider.set([value, this._endPoint]);
        }
        this._startPoint = value;
    }
    get startPoint() {
        return this._startPoint;
    }

    @Input('end-point')
    set endPoint(value: string) {
        if (this.slider) {
            this.slider.noUiSlider.set([this._startPoint, value]);
        }
        this._endPoint = value;
    }
    get endPoint() {
        return this._endPoint;
    }

    constructor(private elementRef: ElementRef) { }

    ngOnInit() {
        this.slider = jQuery(this.elementRef.nativeElement).find('.rangeSlider')[0];

        if (this.range.length > 1) {
            var that = this;
            noUiSlider.create(this.slider, {
                start: [this.startPoint, this.endPoint],
                step: 1,
                range: {
                    'min': [0],
                    'max': [this.range.length - 1]
                },
                connect: true,
                animate: true,
                animationDuration: 400,
                pips: {
                    mode: 'steps',
                    density: 10,
                    format: {
                        to: function (value: number) {
                            return that.range[Math.round(value)];
                        },
                        from: function (value: string) {
                            return that.range.indexOf(value);
                        }
                    }
                },
                tooltips: [false, false],
                format: {
                    to: function (value: number) {
                        return that.range[Math.round(value)];
                    },
                    from: function (value: string) {
                        return that.range.indexOf(value);
                    }
                },
            });
            this.slider.noUiSlider.on('change.one', function (values: Array<string>, changed: number) {
                let event = new RangeSliderChange();
                event.point = (changed === 0) ? 'start' : 'end';
                event.newValue = values[changed];
                that.slide.emit(event);
                setTimeout(() => {
                    if (values[0] != that._startPoint || values[1] != that._endPoint) {
                        that.slider.noUiSlider.set([that._startPoint, that._endPoint]);
                    }
                }, 0);
            });
        }
    }
}
