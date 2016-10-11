import {Component, OnInit, Input} from '@angular/core';

interface SwitchSelectorValue {
    value: number|string;
    name: string;
    selected?: boolean;
}

@Component({
    selector: 'switch-selector',
    templateUrl: './switch-selector.component.html',
    styleUrls: ['./switch-selector.component.css']
})
export class SwitchSelectorComponent implements OnInit {

    // TODO Review necessity of private properties '_d', '_c'

    private _d: Array<SwitchSelectorValue> = [];

    private _c: Object = {};

    private checked: boolean = null;

    @Input() set data(d: Array<SwitchSelectorValue>) {
        this._d = d;
        this.checked = null;
        this._d.forEach(function(el, i){
            if (el['selected'] === true && this.checked === null) {
                this.checked = (i === 0) ? false : true;
            } else {
                this._d[i]['selected'] = false;
            }
        }, this);
    }

    @Input() set config(c: Object) {
        this._c = c;
    }

    onChange(index?: number) {
        let oldValue = this.checked;
        switch (index) {
            case 1:
                this.checked = true;
            break;
            case 0:
                this.checked = false;
            break;
            default:
                this.checked = !this.checked;
            break;
        }
        if (oldValue !== this.checked) {
            console.log('SwitchSelectorComponent changed to ' + this.checked);
        }
    }

    constructor() {
    }

    ngOnInit() {
    }

}
