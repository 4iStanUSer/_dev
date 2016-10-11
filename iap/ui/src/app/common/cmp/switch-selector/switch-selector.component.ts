import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';

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

    @Output() changed = new EventEmitter();

    @Input() set data(d: Array<SwitchSelectorValue>) {
        if (d.length != 2) {
            console.error('SwitchSelectorComponent incorrect input data');
            return;
        }
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
            let value = (this.checked === true)
                    ? this._d[1]['value'] : this._d[0]['value'];
            this.changed.emit({
                'value': value
            });
            console.log('SwitchSelectorComponent changed to ' + value);
        }
    }

    constructor() {
    }

    ngOnInit() {
    }

}
