import {Component, OnInit, OnChanges, Input, SimpleChanges} from '@angular/core';
import {
    SelectorModel,
    SelectorItemModel
} from "./../selector.model";
import {Helper} from "../../../../common/helper";

@Component({
    selector: 'hierarchical-selector',
    templateUrl: './hierarchical-selector.component.html',
    styleUrls: ['./hierarchical-selector.component.css']
})
export class HierarchicalSelectorComponent implements OnInit, OnChanges {

    @Input() model: SelectorModel;

    private rootLevelItems: Array<SelectorItemModel> = [];
    private items: Array<SelectorItemModel> = [];
    private itemsToShow: Array<SelectorItemModel> = [];

    private searchText: string = null;

    private lang: Object = {
        'items_title': 'Categories',
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

    ngOnChanges(ch: SimpleChanges) {
        if (ch['model']) {
            this.rootLevelItems = this.model.getFirstLevelItems();
            this.items = this.model.getFlatListItems();
            this.itemsToShow = this.getFilteredItems(this.searchText);
        }
    }

    private getFilteredItems(searchText: string = null) {

        if (searchText && searchText.length) {
            this.rootLevelItems.forEach((item) => {
                item.hideToBottom();
            }, this);

            let items = this.items.filter((item) => {
                return (item.name.toLowerCase().indexOf(searchText) != -1);
            }, this);

            items.forEach((item) => {
                item.showToUp();
            }, this);

            return this.items.filter((item) => {
                return !(item.isHidden);
            }, this);
        } else {

            this.rootLevelItems.forEach((item) => {
                item.showToBottom();
            }, this);

            return this.items.filter((item) => {
                return !(item.isHidden);
            }, this);
        }
    }

    private range(count: number) {
        return Helper.range(count);
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

    private changeExpandStatus(item: SelectorItemModel) {
        item.changeExpandStatus();
        this.itemsToShow = this.getFilteredItems(this.searchText);
    }

}
