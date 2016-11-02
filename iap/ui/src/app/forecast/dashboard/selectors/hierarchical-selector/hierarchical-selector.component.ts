import {Component, OnInit, Input} from '@angular/core';
import {SelectorModel} from "../selectors.component";

@Component({
    selector: 'hierarchical-selector',
    templateUrl: './hierarchical-selector.component.html',
    styleUrls: ['./hierarchical-selector.component.css']
})
export class HierarchicalSelectorComponent implements OnInit {

    @Input() data: SelectorModel;

    constructor() {
    }

    ngOnInit() {
    }

}
