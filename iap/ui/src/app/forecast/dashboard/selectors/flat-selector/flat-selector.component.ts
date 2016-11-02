import {Component, OnInit, Input} from '@angular/core';
import {SelectorModel} from "../selectors.component";

@Component({
    selector: 'flat-selector',
    templateUrl: './flat-selector.component.html',
    styleUrls: ['./flat-selector.component.css']
})
export class FlatSelectorComponent implements OnInit {

    @Input() data: SelectorModel;

    constructor() {
    }

    ngOnInit() {
    }

}
