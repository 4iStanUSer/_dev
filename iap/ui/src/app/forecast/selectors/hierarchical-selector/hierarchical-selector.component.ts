import {Component, OnInit, OnChanges, Input, SimpleChanges, EventEmitter} from '@angular/core';
import {
    SelectorModel,
    SelectorItemModel
} from "./../selector.model";
import {Helper} from "../../../common/helper";
import {Output} from "@angular/core/src/metadata/directives";

@Component({
    selector: 'hierarchical-selector',
    templateUrl: './hierarchical-selector.component.html',
    styleUrls: ['./hierarchical-selector.component.css']
})
export class HierarchicalSelectorComponent implements OnInit, OnChanges {

    @Input() model: SelectorModel;
    @Output() nothingSelected =  new EventEmitter<boolean>();

    private rootLevelItems: Array<SelectorItemModel> = [];
    private items: Array<SelectorItemModel> = [];
    private itemsToShow: Array<SelectorItemModel> = [];

    private searchText: string = null;

    constructor() {
    }

    ngOnInit() {
        // console.log('hie selectors init started');
        // console.log(this.model);
        // console.log('hie selectors init ended');
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['model']) {
            //console.log("ngOnChanges HierarchicalSelectorComponent");
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
        let totalId = "all";
        if(item.id == totalId){
            //var result = objArray.map(function(a) {return a.foo;});
            let idsArray = this.items.map(function(a) {return a.id;});
            if (item.isSelected) {
                this.model.deselect(idsArray);
            }
            else {
                this.model.select(idsArray);
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
        this.selectionChangedEmit();
        // if (this.model.selected.length == 0){
        //     this.nothingSelected.emit(true);
        // }
        // else{
        //     this.nothingSelected.emit(false);
        // }
        //console.log("click - selected items", this.model.selected.length);

    }

    private onDeselectItemClick(item_id: string) {
        let totalId = "all";
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
        this.selectionChangedEmit();
        //console.log("desel - selected items", this.model.selected.length);
    }

    private selectionChangedEmit(){
        if (this.model.selected.length == 0){
            this.nothingSelected.emit(true);
        }
        else{
            this.nothingSelected.emit(false);
        }
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
