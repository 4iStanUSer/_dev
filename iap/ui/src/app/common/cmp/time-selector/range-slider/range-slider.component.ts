import {Component, OnInit, Input, Output, ElementRef, Renderer, SimpleChanges, OnChanges, EventEmitter} from '@angular/core';
import {Sliders} from "./../time-selector.component";

interface Point {
    full_name: string,
    short_name: string,
    timescale: string
}


interface Coordinate {
    start: number;
    end: number;
    checkpoint: number;
    point_idx: number;
}


@Component({
    selector: 'range-slider',
    templateUrl: './range-slider.component.html',
    styleUrls: ['./range-slider.component.css']
})
/**
 * Component for DRAWING time line (range of time points).
 * It uses SVG to draw the time line.
 */
export class RangeSliderComponent implements OnInit, OnChanges {

    /**
     * Flag middle time point (slider).
     * @type {boolean}
     */
    private hasMid: boolean = false;

    /**
     * Link to html element in DOM.
     * @type {any}
     */
    private element: HTMLElement = null;

    /**
     * List of points to draw. Contains only data from upper component
     * @type {Array<Point>}
     */
    private points: Array<Point> = null;

    /**
     * Storage for all sliders
     * @type {any}
     */
    private sliders: Sliders = null;

    /**
     * Info about container of drawing
     * @type {Object}
     */
    private easelDetails: Object = null;

    /**
     * List of coordinates for time line (track).
     * Coordinates have 2 variants:
     * - inside container for drawing
     * - inside page
     * @type {any}
     */
    private trackCoords: {
        svg: Array<Coordinate>,
        page: Array<Coordinate>} = null;

    /**
     * Base configuration for drawing
     * @type {{height: number; trackY: number; trackSideMargin: number; sliderHeight: number; sliderWidth: number}}
     */
    private svgConfig: Object = {
        height: 40,
        trackY: 30,
        trackSideMargin: 10,
        sliderHeight: 25,
        sliderWidth: 15,
    };

    /**
     * Set of string commands for SVG
     * @type {{track: any; sliders: any}}
     */
    private svgData = {
        track: null,
        sliders: null
    };

    /**
     * Shows selected indexes in this.trackCoords
     * @type {any}
     */
    private selectedIndexes: Object = null;

    @Input() data: Array<Point>;
    @Input() selected: Sliders;

    @Output() changed: EventEmitter<{
        slider: string,
        value: Point
    }>= new EventEmitter();

    constructor(private elRef: ElementRef, private renderer: Renderer) {
        this.element = elRef.nativeElement;
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        console.info('SliderComponent: ngOnChanges()');
        if (ch['data']) {
            this.points = ch['data']['currentValue'];
        }
        if (ch['selected']) {
            this.sliders = ch['selected']['currentValue'];
        }
        let correspond = {};
        for (let slider in this.sliders) {
            let idx = this.points.indexOf(this.sliders[slider]);
            if (idx == -1) {
                correspond = false
            } else {
                correspond[slider] = idx;
            }
        }

        this.hasMid = (this.sliders['mid']) ? true : false;
        if (!this.easelDetails) {
            this.easelDetails = this.getEaselDetails();
        }
        if (correspond !== false) {
            this.selectedIndexes = correspond;
            this.calculate();
        }
    }

    /**
     * Finalizes changing of slider position on time line
     * and fires 'changed' event to upper component.
     * @param slider
     * @param pointIndex
     */
    private selectPoint(slider: string, pointIndex: number) {
        if (!this.points[pointIndex]) return;

        this.selectedIndexes[slider] = pointIndex;
        this.svgData['sliders'][slider] =
            this.getSvgSliderCmds(
                {
                    x: this.trackCoords['svg'][pointIndex]['checkpoint'],
                    y: this.svgConfig['trackY']
                }
            );
        this.changed.emit({
            slider: slider,
            value: this.points[pointIndex]
        });
    }

    /**
     * Handles 'mousedown' event on slider, attaches 'mouseup' event,
     * run re-draw of slider if it was moved.
     * @param slider
     * @param e
     */
    private onSliderMousedown(slider: string, e: MouseEvent) {
        let baseX = e.pageX;
        let list = this.renderer.listenGlobal(
            'document', 'mousemove', (e) => {
                let pageX = e.pageX;
                let curr = this.trackCoords['page'][this.selectedIndexes[slider]];

                if (pageX <= curr['end'] && pageX >= curr['start']) {
                    return;
                }
                let startIdx = 0;
                let endIdx = this.trackCoords['page'].length;
                if (slider == 'start') {
                    if (this.hasMid) {
                        endIdx = this.selectedIndexes['mid'];
                    } else {
                        endIdx = this.selectedIndexes['end'];
                    }
                } else if (slider == 'end') {
                    if (this.hasMid) {
                        startIdx = this.selectedIndexes['mid'] + 1;
                    } else {
                        startIdx = this.selectedIndexes['start'] + 1;
                    }
                } else if (slider == 'mid') {
                    startIdx = this.selectedIndexes['start'] + 1;
                    endIdx = this.selectedIndexes['end'];
                }


                for ( let i = startIdx; i < endIdx; i++ ) {
                    let c = this.trackCoords['page'][i];
                    if (pageX <= c['end'] && pageX >= c['start']) {
                        this.selectPoint(slider, i);
                        break;
                    }
                }

                // console.log(event);
            });
        let list1 = this.renderer.listenGlobal(
            'document', 'mouseup', (e) => {
                list();
                list1();
            });
    }

    /**
     * Calculates all coordinates for drawing, based on:
     * - container's width;
     * - count of time points.
     */
    private calculate() {
        // L - count of points
        // W - width of container
        // (L-2)*3x + (L-2+1)*x + 2x = W ---> x = W/(4L-5)

        let x: number = 0;
        let w = this.easelDetails['width'];
        let margin = this.svgConfig['trackSideMargin'];
        if (this.points.length > 1) {
            x = (w - 2 * margin) / (4 * this.points.length - 5);

            let f = margin;
            this.trackCoords = {
                'svg': [],
                'page': []
            };
            this.trackCoords['svg'].push({
                'start': f,
                'end': f + x,
                'checkpoint': (f + x / 2),
                'point_idx': 0
            });
            f += x + x;
            for (let i = 1; i < this.points.length - 1; i++) {
                this.trackCoords['svg'].push({
                    'start': f,
                    'end': f + (3 * x),
                    'checkpoint': (f + (3 * x) / 2),
                    'point_idx': i
                });
                f += (3 * x) + x;
            }
            this.trackCoords['svg'].push({
                'start': f,
                'end': f + x,
                'checkpoint': (f + x / 2),
                'point_idx': this.points.length - 1
            });
            this.trackCoords['page'] = this.trackCoords['svg'].map((el) => {
                return {
                    'start': el['start'] + this.easelDetails['left'],
                    'end': el['end'] + this.easelDetails['left'],
                    'checkpoint': el['checkpoint'] + this.easelDetails['left'],
                    'point_idx': el['point_idx']
                };
            }, this);

            this.svgData['track'] = this.getSvgTrackCmds(
                this.trackCoords['svg'], this.svgConfig['trackY']);

            this.svgData['sliders'] = {};
            for (let slider in this.sliders) {
                let idx = this.points.indexOf(this.sliders[slider]);
                if (idx != -1) {
                    this.selectPoint(slider, idx);
                }
            }
        } else if (this.points.length == 1) {
            x = (w - 2 * margin);
        } else {
            // TODO Kill view
        }

        // console.log(this.trackCoords);

    }

    /**
     * Returns details of container for drawing
     * @returns {{right: any, left: any, width: number}}
     */
    private getEaselDetails() {
        let trackElement = this.element.querySelector('.track');
        let dims = trackElement.getBoundingClientRect();
        return {
            right: dims['right'],
            left: dims['left'],
            width: dims['width']
                ? dims['width'] : (dims['right'] - dims['left'])
        };
    }

    /**
     * Returns string with commands for SVG container to draw time points line
     * @param coords
     * @param yLine
     * @returns {string}
     */
    private getSvgTrackCmds(coords: Array<Object>, yLine: number): string {
        let comm = "";
        for (let i = 0; i < coords.length; i++) {
            comm += ' M ' + (coords[i]['start']) + ' ' + yLine + ' H ' + (coords[i]['end']);
        }
        return comm;
    }

    /**
     * Returns string with commands for SVG container to draw one slider
     * @param coords
     * @returns {string}
     */
    private getSvgSliderCmds(coords: {x: number, y: number}) {
        let sliderW = this.svgConfig['sliderWidth'];
        let sliderH = this.svgConfig['sliderHeight'];
        let comm = [];
        comm.push(this.toStr(coords['x']) + ',' + this.toStr(coords['y']));
        comm.push(this.toStr(coords['x'] - sliderW/2) + ',' + this.toStr(coords['y'] - sliderH/3));
        comm.push(this.toStr(coords['x'] - sliderW/2) + ',' + this.toStr(coords['y'] - sliderH));
        comm.push(this.toStr(coords['x'] + sliderW/2) + ',' + this.toStr(coords['y'] - sliderH));
        comm.push(this.toStr(coords['x'] + sliderW/2) + ',' + this.toStr(coords['y'] - sliderH/3));
        comm.push(this.toStr(coords['x']) + ',' + this.toStr(coords['y']));
        return comm.join(' ');
    }

    private toStr(exp: any): string {
        return exp.toString();
    }

    /**
     * Sorry, not documented yet!
     * @param o
     * @returns {string[]}
     */
    private getKeys(o: Object) {
        return Object.keys(o);
    }
}
