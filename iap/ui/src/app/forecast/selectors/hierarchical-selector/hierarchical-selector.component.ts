import {Component, OnInit, OnChanges, Input, SimpleChanges} from '@angular/core';
import {
    SelectorModel,
    SelectorItemModel
} from "./../selector.model";
import {Helper} from "../../../common/helper";

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

    // private lang: Object = {
    //     'items_title': 'Categories',
    //     'search_title': 'Search',
    //     'search_placeholder': 'Type here',
    //     'search_clear': 'Clear search',
    //     'selected_title': 'Selected',
    //     'not_found_items': 'Not found items',
    //     'apply_button': 'Apply',
    //     'cancel_button': 'Cancel'
    // };

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
    ngAfterViewChecked(){
        //console.log("ngAfterViewChecked HierarchicalSelectorComponent");
        //add variable to pass if changes were done and only in that case call the following
        //this method is being called too often
        this.rootLevelItems = this.model.getFirstLevelItems();
        this.items = this.model.getFlatListItems();
        this.itemsToShow = this.getFilteredItems(this.searchText);
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
        let totalId = "*";
        if(item.id == totalId){
            //var result = objArray.map(function(a) {return a.foo;});
            let idsArray = this.items.map(function(a) {return a.id;});
            if (item.isSelected) {
                this.model.deselect(idsArray);
                //this.model.isAnythingSelected = false;
            }
            else {
                this.model.select(idsArray);
                //this.model.isAnythingSelected = true;
            }
        }
        else {
            if (item.isSelected) {
                this.model.deselect([item.id]);
                if ( (this.model.flatListItems.length - this.model.selected.length) == 1 ){
                    this.model.deselect([totalId]);
                }
            } else {
                this.model.select([item.id]);
                //this.model.isAnythingSelected = true;
                if ( (this.model.flatListItems.length - this.model.selected.length) == 1 ){
                    this.model.select([totalId]);
                }
            }
        }
        console.log("click - selected items", this.model.selected.length);

    }

    private onDeselectItemClick(item_id: string) {
        let totalId = "*";
        if(item_id == totalId){
            //var result = objArray.map(function(a) {return a.foo;});
            let idsArray = this.items.map(function(a) {return a.id;});
            this.model.deselect(idsArray);
        }
        else {
            this.model.deselect([item_id]);
            if ( (this.model.flatListItems.length - this.model.selected.length) == 1 ){
                this.model.deselect([totalId]);
            }
        }
        console.log("desel - selected items", this.model.selected.length);
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
