import {Component, OnInit, Input} from '@angular/core';
import {
    SelectorModel,
    SelectorItemModel
} from "./../../../../common/model/selector.model";

@Component({
    selector: 'hierarchical-selector',
    templateUrl: './hierarchical-selector.component.html',
    styleUrls: ['./hierarchical-selector.component.css']
})
export class HierarchicalSelectorComponent implements OnInit {

    @Input() model: SelectorModel;

    private items: Array<SelectorItemModel> = [];
    // private itemsToShow: Array<SelectorItemModel> = [];

    private lang: Object = {
        'items_title': 'Brands',
        'search_title': 'Search',
        'search_placeholder': 'Type here',
        'search_clear': 'Clear search',
        'selected_title': 'Selected',
        'not_found_items': 'Not found items'
    };

    constructor() {
    }

    ngOnInit() {
    }

}
