import { Component, Input, Output, EventEmitter } from '@angular/core';
import {TreeComponent} from './tree/';
import {SearchComponent} from './search/';

//TODO - tree and search component depends on same inputed data structure - REFACTOR
//TODO - change event name from itemSelected to changeSelection

@Component({
    moduleId: module.id,
    selector: 'hierarchy-widget',
    directives: [TreeComponent, SearchComponent],
    template: `
    <div class="widget-container">
        <div class="container-fluid">
            <search [items]="items" (nodeSelected)="searchNodeSelected($event)"></search>
        </div>
        <div class="container-fluid tree-container">
            <tree [items]="items" [forcedSelect]="_searchSelected" (changeSelection)="treeNodeSelected($event)" (currentSelection)="nowSelected($event)"></tree>
        </div>
    </div>
    `,
    styles: [ `
.widget-container {
    position:relative;
    border:1px solid #ccc;
    padding: 10px;
}
.tree-container {
    margin-top:10px;
}
`
    ]
})
export class HierarchyWidgetComponent {
    @Input() items: Array<Object>;

    @Output() itemSelected = new EventEmitter();
    @Output() currentSelection = new EventEmitter();

    private _searchSelected: string = null;
    // private

    constructor() { }

    treeNodeSelected(selected_id: string) {
        console.info('HierarchyWidget Component, in tree selected item');

        this.itemSelected.emit({
            'id': selected_id
        });
    }

    searchNodeSelected(selected: Object) {
        console.info('HierarchyWidget Component, in search selected item');
        this._searchSelected = selected['id'];
    }

    nowSelected(selection){
        this.currentSelection.emit(selection);
    }
}
