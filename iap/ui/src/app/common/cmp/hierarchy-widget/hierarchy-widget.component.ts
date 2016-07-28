import { Component, Input, Output, OnInit, ElementRef,
    EventEmitter } from '@angular/core';
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
            <tree [items]="items" [forcedSelect]="_searchSelected" (changeSelection)="treeNodeSelected($event)"></tree>
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
export class HierarchyWidgetComponent implements OnInit {
    @Input() items: Array<Object>;

    @Output() itemSelected = new EventEmitter();

    private _searchSelected: string = null;

    constructor(private elementRef: ElementRef) { }

    ngOnInit() {
        //console.log(this.items)
    }

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
}
