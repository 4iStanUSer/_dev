import { Component, Input, Output,
    ElementRef, Renderer, EventEmitter} from '@angular/core';
import * as _ from 'lodash';

// TODO Occur window scroll on switch between items - fix it

class DropdownConfig {
    multiple: boolean = false;
    search_field: boolean = true;

    constructor(config = {}) {
        _.extend(this, config);
    }
}

class DropdownItem {
    public elRef: ElementRef;
    public index: number = null;
    constructor(public id: string, public label: string,
        public isDisabled: boolean, public isSelected: boolean = false) { }
}

@Component({
    moduleId: module.id,
    selector: 'dropdown',
    templateUrl: 'dropdown.component.html',
    styleUrls: ['dropdown.component.css']
})
export class DropdownComponent {
    private config: DropdownConfig = new DropdownConfig();
    private _items: Array<any> = [];
    private filteredItems: Array<DropdownItem> = [];
    private expandedStatus: boolean = false;
    private hoveredIndex: number = null;
    private selected: Array<DropdownItem> = [];
    private selectedAtStart: Array<DropdownItem> = [];

    private bodyKeysListener: Function = null;
    private bodyClickListener: Function = null;

    @Input() set items(items: Array<any>) {
        this._items = items; // May DO some transformation
        this.makeDropdownList(items);
    };

    @Input() set configuration(config: DropdownConfig) {
        this.config = new DropdownConfig(config);
    };
    @Output() changeSelection = new EventEmitter();

    constructor(private rndr: Renderer, private elRef: ElementRef) { }

    ngOnDestroy() {
        this.expandedStatus = true;
        this.toggleExpandedStatus(null);
    }

    makeDropdownList(items: Array<Object>) {
        this.selected = [];
        this.filteredItems = items.map((item, i) => {
            let is_disabled = (item['state'] && item['state']['disabled']) ?
                true : false;
            let newItem = new DropdownItem(item['id'], item['text'],
                is_disabled);

            if (item['state'] && item['state']['selected']) {
                if (this.config.multiple ||
                    (
                        !this.config.multiple
                        &&
                        this.selected.length == 0
                    )
                ) {
                    if (this.selected.indexOf(newItem) == -1) {
                        newItem.isSelected = true;
                        this.selected.push(newItem);
                    }
                }
            }
            newItem.index = i;
            return newItem;
        });
    }

    toggleExpandedStatus($event) {
        this.expandedStatus = !this.expandedStatus;
        if (!this.expandedStatus) {
            this.hoveredIndex = null;

            if (this.bodyKeysListener != null) {
                this.bodyKeysListener();
                this.bodyKeysListener = null;
            }
            if (this.bodyClickListener != null) {
                this.bodyClickListener();
                this.bodyClickListener = null;
            }
        } else {
            this.selectedAtStart = this.selected;
            this.rndr.invokeElementMethod(this.elRef.nativeElement, 'focus');
            if (this.bodyKeysListener == null) {
                this.bodyKeysListener = this.rndr.listenGlobal(
                    'document', 'keyup', (event) => {
                        this._attachSpecKeysListeners(event)
                    });
            }
            if (this.bodyClickListener == null) {
                this.bodyClickListener = this.rndr.listenGlobal(
                    'document', 'click', (event) => {
                        if (!this.elRef.nativeElement.contains(event.target)) {
                            //if (this.selectedAtStart != this.selected) {
                            //    this.selected = this.selectedAtStart;
                            //}
                            if (this.selectedAtStart != this.selected) {
                                if (this.selectedAtStart[0]) {
                                    this.switchSelectionForSingleDropdown(this.selectedAtStart[0].index);
                                } else {
                                    this.selected[0].isSelected = false;
                                    this.selected = [];
                                }
                            }
                            this.toggleExpandedStatus(event);
                        }
                    });
            }
        }
        //if (!this.config.multiple) { // TODO focus
        //    this.rndr.invokeElementMethod(
        //        this.selected[0].elRef.nativeElement, 'focus');
        //}
    }
    elementClicked(e: Event, index: number, force: boolean = false) {
        if (this.filteredItems && this.filteredItems[index]) {
            if (this.filteredItems[index].isDisabled) {
                console.info('Dropdown element is disabled!');
                return false;
            }
            if (!this.config.multiple) { // For single dropdown
                let switched = this.switchSelectionForSingleDropdown(index);
                if (switched || force) {
                    this.toggleExpandedStatus(e);
                    // Generate event
                    console.info('Dropdown changed selection');
                    let selection = null;
                    if (this.selected[0]) {
                        selection = this.selected[0].id;
                    }
                    this.changeSelection.emit({
                        'selected': selection
                    });
                }
            } else { // TODO For multiple dropdown
            }
        }
    }

    private switchSelectionForSingleDropdown(newIndex: number) {
        let c = this.filteredItems[newIndex];
        let selected = (this.selected[0]) ? this.selected[0] : null;
        let is_new = false;
        if (selected !== c) {
            is_new = true;
            selected.isSelected = false;
            c.isSelected = true;
            this.selected = [];
            this.selected.push(c);
            // TODO focus on element
        }
        return is_new;
    }
    private _attachSpecKeysListeners(e: Event = null) {
        let keyCode = e['keyCode'];
        // Handle special keys
        if (!this.config.multiple) { // For single dropdown
            if (this.filteredItems.length > 0) {
                let index = null;
                let selected
                switch (parseInt(keyCode)) {
                    case 40: //ArrowDown
                        if (this.selected[0] && this.filteredItems.length > this.selected[0].index + 1) {
                            index = this.selected[0].index + 1;
                        } else {
                            index = 0;
                        }
                        this.switchSelectionForSingleDropdown(index);
                        break;
                    case 38: //ArrowUp
                        if (this.selected[0] && this.selected[0].index - 1 >= 0) {
                            index = this.selected[0].index - 1;
                        } else {
                            index = this.filteredItems.length - 1;
                        }
                        this.switchSelectionForSingleDropdown(index);
                        break;
                    case 13: // Enter
                        if (this.selected[0]) {
                            this.elementClicked(e, this.selected[0].index, true);
                        }
                        break;
                    case 27:
                        if (this.selectedAtStart != this.selected) {
                            if (this.selectedAtStart[0]) {
                                this.switchSelectionForSingleDropdown(this.selectedAtStart[0].index);
                            } else {
                                this.selected[0].isSelected = false;
                                this.selected = [];
                            }
                        }
                        this.toggleExpandedStatus(e);
                        break;
                }
            } else if (this.bodyKeysListener != null) {
                this.bodyKeysListener();
                this.bodyKeysListener = null;
            } else {
                console.warn('Have no action!');
            }
        } else { // TODO For multiple dropdown
        }

    }
}
