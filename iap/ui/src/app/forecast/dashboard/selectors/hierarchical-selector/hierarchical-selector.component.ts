import {Component, OnInit, Input} from '@angular/core';
import {SelectorModel} from "../../../../common/model/selector.model";

@Component({
    selector: 'hierarchical-selector',
    templateUrl: './hierarchical-selector.component.html',
    styleUrls: ['./hierarchical-selector.component.css']
})
export class HierarchicalSelectorComponent implements OnInit {

    @Input() model: SelectorModel;

    constructor() {
    }

    ngOnInit() {
    }

}
