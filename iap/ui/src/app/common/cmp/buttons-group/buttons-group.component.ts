import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges,
    Input,
    Output,
    EventEmitter
} from '@angular/core';


interface ButtonDataInput {
    id: string|number;
    name: string;
    selected?: boolean;
}
interface ButtonDataChangeOutput extends ButtonDataInput {
}

@Component({
    selector: 'buttons-group',
    templateUrl: './buttons-group.component.html',
    styleUrls: ['./buttons-group.component.css']
})
export class ButtonsGroupComponent implements OnInit, OnChanges {

    @Input() data: Array<ButtonDataInput> = [];

    @Output() change: EventEmitter<ButtonDataChangeOutput> = new EventEmitter();

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
            console.info('-->ButtonsGroupComponent -> change()');
            this.selected = index;
            this.change.emit({
                'id': this.data[this.selected]['id'],
                'name': this.data[this.selected]['name']
            });
        }
    }
}