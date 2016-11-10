import { Component, Input, Output, EventEmitter } from '@angular/core';

//TODO - tree and search component depends on same inputed data structure - REFACTOR
//TODO - change event name from itemSelected to changeSelection

@Component({
    selector: 'hierarchy-widget',
    styleUrls: ['hierarchy-widget.component.css'],
    templateUrl: 'hierarchy-widget.component.html',
})
export class HierarchyWidgetComponent {
    @Input() items: Array<Object>;

    @Output() itemSelected = new EventEmitter();
    @Output() currentSelection = new EventEmitter();

    private _searchSelected: string = null;

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
