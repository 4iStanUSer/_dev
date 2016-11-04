import {Component, OnInit, OnChanges, Input, SimpleChanges} from '@angular/core';

import {
    SelectorItemModel,
    SelectorModel
} from "../../../../common/model/selector.model";

@Component({
    selector: 'flat-selector',
    templateUrl: './flat-selector.component.html',
    styleUrls: ['./flat-selector.component.css']
})
export class FlatSelectorComponent implements OnInit, OnChanges {

    @Input() model: SelectorModel;

    private lang: Object = {
        'items_title': 'Brands',
        'search_title': 'Search',
        'search_placeholder': 'Type here',
        'search_clear': 'Clear search',
        'selected_title': 'Selected',
        'not_found_items': 'Not found items'
    };

    private items: Array<SelectorItemModel> = [];
    private itemsToShow: Array<SelectorItemModel> = [];

    private searchText: string = null;

    constructor() {
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['model']) {
            this.items = this.model.getFirstLevelItems();
            // Filter if search isn't empty
            this.itemsToShow = this.getFilteredItems(this.searchText);
        }
    }

    private onItemClick(item: SelectorItemModel) {
        if (item.isSelected) {
            this.model.deselect([item.id]);
        } else {
            this.model.select([item.id]);
        }
    }

    private onDeselectItemClick(item_id: string) {
        this.model.deselect([item_id]);
    }

    private onSearchTextChange(text: string) {
        this.searchText = text;
        this.itemsToShow = this.getFilteredItems(this.searchText);
    }

    private getFilteredItems(searchText: string = null) {
        if (searchText && searchText.length) {
            return this.items.filter((item) => {
                return (item.name.toLowerCase().indexOf(searchText) != -1);
            }, this);
        }
        return this.items;
    }
}
