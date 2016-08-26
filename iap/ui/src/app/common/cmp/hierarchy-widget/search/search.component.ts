import { Component, Input, Output, ViewChild,
    OnChanges, OnDestroy, AfterViewInit,
    ElementRef, Renderer, EventEmitter } from '@angular/core';


@Component({
    // moduleId: module.id,
    selector: 'search',
    styleUrls: ['search.component.css'],
    template: `
        <input #searchField type="text" class="form-control" [(ngModel)]="inputted" (keyup)="_onKeyup(inputted, $event)">
        <div class="variants-container" *ngIf="_showNodesStatus">
            <span *ngIf="_nodesFiltered.length==0">
                No match
            </span>
            <ul class="nodes-container" *ngIf="_nodesFiltered.length>0">
                <li 
                    class="search-node"
                    [class.is_hovered]="node.isHovered"
                    [class.is_disabled]="node.isDisabled"

                    *ngFor="let node of _nodesFiltered; let i = index"
                
                    (click)="_onSelect(i)"
                    (mouseenter)="_onHover(i)"
                    >{{ node.text }}</li>
            </ul>
        </div>
    `,
})
export class SearchComponent implements OnChanges, AfterViewInit, OnDestroy {

    // @Input() items: Array<Object>;
    @Input() set items(items: Array<Object>) {
        this.inputted = '';
        this.hoverIndex = null;
        this._nodesFiltered = [];
        this._nodes = this._initNodesFromItems((items) ? items : []);
    }

    @Output() nodeSelected = new EventEmitter();

    @ViewChild('searchField') searchField: ElementRef;

    private inputted: string = '';

    private hoverIndex: number = null;
    private _showNodesStatus: Boolean = false;
    private _nodes: Array<SearchNode> = [];
    private _nodesFiltered: Array<SearchNode> = [];

    private bodyClickListener: Function = null;
    private bodyKeysListener: Function = null;

    constructor(private _elementRef: ElementRef, private _renderer: Renderer) { }

    ngAfterViewInit() {
        //console.log(this.searchField);
    }
    ngOnChanges(changes) {
        // let items = (changes.items) ? changes.items.currentValue : [];
        // this._nodes = this._initNodesFromItems(items);
    }
    ngOnDestroy() {
        this._closeContainer();
    }

    private _initNodesFromItems(items: Array<Object>): Array<SearchNode> {
        let nodes: Array<SearchNode> = [];
        let children: Array<SearchNode>;
        let node: SearchNode;

        if (items && items.length) {
            for (let i = 0; i < items.length; i++) {
                let item = items[i];
                let isDisabled = (item['state'] && item['state']['disabled'])
                    ? true : false;
                node = new SearchNode(item['type'], item['id'],
                    item['text'], isDisabled);

                nodes.push(node);

                if (item['children']) {
                    children = this._initNodesFromItems(item['children']);
                    nodes = nodes.concat(children)
                }
            }
        }
        return nodes;
    }
    private _attachSpecKeysListeners(e: Event = null) {
        let keyCode = e['keyCode'];
        // Handle special keys
        if (this._nodesFiltered && this._nodesFiltered.length > 0) {
            let index = null;
            switch (parseInt(keyCode)) {
                case 40: //ArrowDown
                    if (this.hoverIndex == null ||
                        this._nodesFiltered.length == this.hoverIndex + 1) {
                        index = 0;
                        this._renderer.invokeElementMethod(
                            this.searchField.nativeElement, 'blur');
                    } else if (this._nodesFiltered[this.hoverIndex + 1]) {
                        index = this.hoverIndex + 1;
                    } else { }
                    this._onHover(index);
                    break;
                case 38: //ArrowUp
                    if (this.hoverIndex == null) {
                        index = this._nodesFiltered.length - 1;
                    } else if (this._nodesFiltered[this.hoverIndex - 1]) {
                        index = this.hoverIndex - 1;
                    } else if (this.hoverIndex - 1 < 0) {
                        index = null;
                        this._renderer.invokeElementMethod(
                            this.searchField.nativeElement, 'focus');
                    } else { }
                    this._onHover(index);
                    break;
                case 13: // Enter
                    if (this.hoverIndex != null &&
                        this._nodesFiltered[this.hoverIndex]) {
                        this._onSelect(this.hoverIndex);
                    }
                    break;
            }
        } else if (this.bodyKeysListener != null) {
            this.bodyKeysListener();
            this.bodyKeysListener = null;
        } else {
            console.warn('Have no action!');
        }
    }
    private _closeContainer(e: Event = null) {
        this.inputted = null;
        this._showNodesStatus = false;
        if (this.hoverIndex != null) {
            if (this._nodesFiltered[this.hoverIndex]) {
                this._nodesFiltered[this.hoverIndex].isHovered = false;
            }
            this.hoverIndex = null;
        }
        this._nodesFiltered = [];
        if (this.bodyClickListener != null) {
            this.bodyClickListener();
            this.bodyClickListener = null;
        }
        if (this.bodyKeysListener != null) {
            this.bodyKeysListener();
            this.bodyKeysListener = null;
        }
    }

    private _onKeyup(text: string, e: Event) {
        if (text && text.length) {
            this._nodesFiltered = this._nodes
                .filter(node => node.text.indexOf(text) !== -1);
            this._showNodesStatus = true;
            if (this._nodesFiltered && this._nodesFiltered.length > 0) {
                if (this.bodyClickListener == null) {
                    this.bodyClickListener = this._renderer.listenGlobal(
                        'document', 'click', (event) => {
                            if (!this._elementRef.nativeElement.contains(event.target)) {
                                this._closeContainer(event)
                            }
                        });
                }
                if (this.bodyKeysListener == null) {
                    this.bodyKeysListener = this._renderer.listenGlobal(
                        'document', 'keyup', (event) => {
                            this._attachSpecKeysListeners(event)
                        });
                }
                return;
            } // TODO REMAKE
        } else {
            this._closeContainer();
        }
    }
    private _onHover(index: number) {
        if (index != null) {
            let justHovered = this._nodesFiltered[index];
            if (justHovered) {
                if (this.hoverIndex != null && index != this.hoverIndex) {
                    this._nodesFiltered[this.hoverIndex].isHovered = false;
                }
                this.hoverIndex = index;
                this._nodesFiltered[this.hoverIndex].isHovered = true;
            }
        } else {
            if (this.hoverIndex != null) {
                this._nodesFiltered[this.hoverIndex].isHovered = false;
            }
            this.hoverIndex = index;
        }
    }

    private _onSelect(index) {
        if (index != null && this._nodesFiltered[index]) {
            let selected = this._nodesFiltered[index];
            if (selected.isDisabled) {
                return console.info('Node is disabled');
            }
            console.info('SearchComponent, selected node - ' + selected['id']);

            // Add unfocus for element
            this._renderer.invokeElementMethod(this.searchField.nativeElement,
                'blur');

            this._closeContainer();
            this.nodeSelected.emit({
                'id': selected['id']
            });
        }

    }
}

class SearchNode {
    public isHovered: boolean = false
    constructor(public type: string, public id: string, public text: string,
        public isDisabled: boolean = false) { }
}

