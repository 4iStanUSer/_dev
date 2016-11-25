import {Component, OnInit, Input} from '@angular/core';
import {SelectorModel} from "./../selector.model";

@Component({
    selector: 'region-selector',
    templateUrl: './region-selector.component.html',
    styleUrls: ['./region-selector.component.css']
})
export class RegionSelectorComponent implements OnInit {

    @Input() model: SelectorModel;

    constructor() {
    }

    ngOnInit() {
    }

}
