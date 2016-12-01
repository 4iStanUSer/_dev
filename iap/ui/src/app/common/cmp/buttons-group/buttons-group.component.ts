import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges,
    Input,
    Output,
    EventEmitter
} from '@angular/core';


// export
interface ButtonDataInput {
    id: string|number;
    name: string;
    selected?: boolean;
}
export type ButtonsGroupDataInput = Array<ButtonDataInput>;

interface ButtonDataChangeOutput extends ButtonDataInput {
}

@Component({
    selector: 'buttons-group',
    templateUrl: './buttons-group.component.html',
    styleUrls: ['./buttons-group.component.css']
})
/**
 * Simple component to show group of buttons.
 * It works as switcher - one time, one choice.
 * Generates event 'changed' when user changed selection inside.
 */
export class ButtonsGroupComponent implements OnInit, OnChanges {

    @Input() data: ButtonsGroupDataInput = [];

    @Output() changed = new EventEmitter(); //ButtonDataChangeOutput

    private selected: string|number = null;

    constructor() {
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['data']) {
            this.selected = null;
            for (let i = 0; i < this.data.length; i++) {
                if (this.selected !== null) {
                    this.data[i]['selected'] = false;
                }
                if (this.data[i]['selected']) {
                    this.selected = i;
                }
            }
        }
    }

    onButtonClick(index: number) {
        if (index != this.selected) {
            console.info('-->ButtonsGroupComponent -> changed()');
            this.selected = index;
            this.changed.emit({
                'id': this.data[this.selected]['id'],
                'name': this.data[this.selected]['name']
            });
        }
    }
}
