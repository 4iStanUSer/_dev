import { Component, Input, Output,
    OnInit, OnChanges, AfterViewInit,
    ElementRef, EventEmitter, ViewEncapsulation } from '@angular/core';
import * as _ from 'lodash';

class TreeOptions {
    multiple: boolean = false;
    mandatory: boolean = true;

    constructor(options = {}) {
        _.extend(this, options);
    }
}


class TreeNodeModel {
    id: string;
    text: string;
    type: string;
    virtual: boolean;
    isSelected: boolean;
    isExpanded: boolean;
    isDisabled: boolean;

    level: number;
    children: Array<TreeNodeModel>;
    hasChildren: boolean = false;
    elementRef: ElementRef;


    constructor(data: Object, public parent: TreeNodeModel, public treeComponent: TreeComponent) {
        this.id = data['id'];
        this.text = data['text'];
        this.type = data['type'];
        this.virtual = !!data['virtual'];
        if (data['state']) {
            this.isSelected = !!data['state']['selected'];
            this.isExpanded = !!data['state']['opened'];
            this.isDisabled = !!data['state']['disabled'];
        } else {
            this.isSelected = false;
            this.isExpanded = false;
            this.isDisabled = false;
        }


        this.level = this.parent ? this.parent.level + 1 : 0;
    }
    setChildren(children: Array<TreeNodeModel>) {
        this.children = children;
        this.hasChildren = !!(children && children.length > 0);
    }
    expandParents(expandThis: boolean = false) {
        if (this.parent) {
            this.parent.expandParents(true)
        }
        if (expandThis) this.isExpanded = true;
    }
}

@Component({
    selector: 'tree-node',
    directives: [TreeNodeComponent],
    //encapsulation: ViewEncapsulation.None,
    styles: [
        '.tree-children { padding-left: 20px }',
        `.node-content-wrapper {
      display: inline-block;
      padding: 2px 5px;
      border-radius: 2px;
      transition: background-color .15s,box-shadow .15s;
    }`,
        '.tree-node-active > .node-content-wrapper { background: #beebff }',
        '.tree-node-active.tree-node-focused > .node-content-wrapper { background: #beebff }',
        '.tree-node-focused > .node-content-wrapper { background: #e7f4f9 }',
        '.node-content-wrapper:hover { background: #f7fbff }',
        '.tree-node-active > .node-content-wrapper, .tree-node-focused > .node-content-wrapper, .node-content-wrapper:hover { box-shadow: inset 0 0 1px #999; }',
        `.toggle-children-placeholder {
        display: inline-block;
        height: 10px;
        width: 10px;
        position: relative;
        top: 1px;
    }`,
        '.toggle-children-button {cursor:pointer}',
        '.node-content-wrapper{cursor:pointer;}',
        '.tree-node-disabled > .node-content-wrapper{color:gray;}',
        '.tree-node-disabled:hover > .node-content-wrapper{cursor:normal;background:none;}',
    ],
    template: `
    <div class="tree-node tree-node-level-{{ node.level }}"
        [class.tree-node-disabled]="node.isDisabled"
        [class.tree-node-active]="node.isSelected">

        <i
            *ngIf="node.hasChildren"
            (click)="toggleExpanded($event)"
            [class.fa-minus]="node.hasChildren && node.isExpanded"
            [class.fa-plus]="node.hasChildren && !node.isExpanded"
            class="fa toggle-children-button" 
            aria-hidden="true"></i>

        <span
        *ngIf="!node.hasChildren"
        class="toggle-children-placeholder">
        </span>
        <div class="node-content-wrapper" (click)="nodeClicked($event)">
            {{ node.text }}
        </div>
      <div class="tree-children" *ngIf="node.isExpanded">
        <div *ngIf="node.children">
          <tree-node *ngFor="let node of node.children" [node]="node"></tree-node>
        </div>
      </div>
    </div>
    `
})
export class TreeNodeComponent implements AfterViewInit {
    @Input() node: TreeNodeModel;

    constructor(private elementRef: ElementRef) { }

    ngAfterViewInit() {
        this.node.elementRef = this.elementRef;
    }
    nodeClicked(e) {
        this.node.treeComponent.nodeCkicked(this.node.id);
    }
    toggleExpanded(e) {
        this.node.isExpanded = !this.node.isExpanded;
    }
}


@Component({
    moduleId: module.id,
    selector: 'tree',
    directives: [TreeNodeComponent],
    encapsulation: ViewEncapsulation.None,
    styles: [
        '.tree-children { padding-left: 20px }'
    ],
    template: `
        <div class="tree">
            <tree-node *ngFor="let node of _nodes" [node]="node"></tree-node>
        </div>
    `
})
export class TreeComponent implements OnChanges {
    private _root: TreeNodeModel;
    private _nodes: Array<TreeNodeModel> = [];
    private _options: TreeOptions = new TreeOptions();
    private _selectedNodes: Array<TreeNodeModel> = [];
    private _mapping: Object = {};

    @Input() set items(items: Array<Object>) { };
    @Input() set options(options: TreeOptions) { };
    @Input() set forcedSelect(node_id: string) { };
    @Output() changeSelection = new EventEmitter();

    constructor() { }

    ngOnChanges(c) {
        console.log('TreeComponent ngOnChanges');
        let options = ('options' in c) ? c.options.currentValue : null;
        let items = ('items' in c) ? c.items.currentValue : null;
        let forcedSelect = ('forcedSelect' in c)
            ? c.forcedSelect.currentValue : null;

        if (options) {
            this._options = new TreeOptions(c['options']);
        }
        if (items) {
            let root = {
                virtual: true,
                id: '#',
                children: (items.length) ? items : []
            };
            this._root = this._generateTree(root, null);
            // get selected nodes
            this._nodes = this._root.children;
        }
        if (forcedSelect) {
            if (forcedSelect == '#') {
                this._deselectAllSelected();
            } else {
                this.selectionProcedure(forcedSelect);
            }
        }
    }

    nodeCkicked(node_id) {
        this.selectionProcedure(node_id);
    }
    selectionProcedure(node_id) {
        if (!this._mapping[node_id])
            return console.error('Have no such node_id');
        if (this._mapping[node_id].isDisabled)
            return console.info('Node is disabled');

        if (!this._options.multiple) { // Single
            let prevSelected = this._selectedNodes[0];
            if (
                !prevSelected
                ||
                (prevSelected
                    &&
                    (
                        prevSelected != this._mapping[node_id]
                    ||
                        !this._options.mandatory
                    )
                )
            ) {
                this._deselectAllSelected();
                if (prevSelected != this._mapping[node_id]) {
                    if (!this._mapping[node_id].isSelected) { // selection
                        this._selectedNodes.push(this._mapping[node_id]);
                    }
                    this._mapping[node_id].isSelected = !this._mapping[node_id].isSelected;
                    if (this._mapping[node_id].isSelected) {
                        this._mapping[node_id].expandParents();
                    }
                }
                // Do Emit
                let e = (this._selectedNodes.length > 0)
                    ? this._selectedNodes[0].id : null;
                this.changeSelection.emit(e);

            }
        } else { // Multiple - TODO
        }
    }

    _deselectAllSelected() {
        // Deselect all previously selected
        for (let i = 0; i < this._selectedNodes.length; i++) {
            this._selectedNodes[i].isSelected = false
        }
        this._selectedNodes = [];
    }

    _generateTree(data: Object, parent: TreeNodeModel): TreeNodeModel {
        let node = new TreeNodeModel(data, parent, this);
        // Add to mapping
        this._mapping[node.id] = node; //// Maybe node path?
        // Add to selected nodes
        if (node.isSelected) {
            this._selectedNodes.push(node); //// Maybe node path?
            // Expand node's parents
            node.expandParents();
        }
        let children = [];
        if (data['children'] && data['children'].length > 0) {
            children = data['children']
                .map(c => this._generateTree(c, node));
        }
        node.setChildren(children);
        return node;
    }
}
