import {Component, OnInit, Input} from '@angular/core';
import {SelectorModel} from "../selectors.component";

@Component({
    selector: 'region-selector',
    templateUrl: './region-selector.component.html',
    styleUrls: ['./region-selector.component.css']
})
export class RegionSelectorComponent implements OnInit {

    @Input() data: SelectorModel;

    constructor() {
    }

    ngOnInit() {
    }

}
