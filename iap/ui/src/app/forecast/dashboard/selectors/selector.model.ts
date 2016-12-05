/**
 * Data Interface for describing one item in any selector
 */
export interface SelectorItemInput {
    name: string;
    id: number|string;
    parent_id: number|string;
}

/**
 * Data Interface for configuration one selector in SelectorsComponent
 */
export interface SelectorConfigInput {
    name: string;
    placeholder: string;
    multiple: boolean;
    type: string; // flat | hierarchical | region
    icon: string;
    disabled?: boolean;
}


/**
 * Model for selector's item (any selector). It contains description of item,
 * links to parent and children and convenient methods for work
 * with item's data and item's parent/children data.
 * It manages only item's data and doesn't know how and where show item!
 */
export class SelectorItemModel {
    id: string = null; //number|
    name: string = null;
    isSelected: boolean = false;
    isHidden: boolean = false;
    isExpanded: boolean = true;
    depth: number = 0;
    icon?: string = null;
    disabled?: boolean = false;

    parent: SelectorItemModel = null;
    children: Array<SelectorItemModel> = [];

    constructor(id: string, name: string,
                icon: string, disabled: boolean) { //number|
        this.id = id;
        this.name = name;
        this.icon = icon;
        this.disabled = !!disabled;
    }

    /**
     * Links this item and his parent.
     * @param parent SelectorItemModel
     */
    addParent(parent: SelectorItemModel) {
        this.parent = parent;
        this.parent.children.push(this);
        this.depth = this.parent.depth + 1;
    }

    /**
     * Changes expand status for this item.
     * Should be used when user clicks on expand/collapse button.
     * Run procedure of hiding/showing for children
     */
    changeExpandStatus() {
        if (this.children && this.children.length) {
            let expandStatus = !this.isExpanded;
            this.isExpanded = expandStatus;

            this.children.forEach((child: SelectorItemModel) => {
                if (false === expandStatus) {
                    child.hideToBottom();
                } else {
                    child.showToBottom();
                }
            });
        }
    }

    /**
     * Shows this item, item's children
     * and sub-children of expanded children
     */
    showToBottom() {
        this.isHidden = false;
        if (this.children && this.children.length) {
            this.children.forEach((child: SelectorItemModel) => {
                if (this.isExpanded) {
                    child.showToBottom();
                } else {
                    child.hideToBottom();
                }
            });
        }
    }

    /**
     * Hides this item and all children.
     */
    hideToBottom() {
        this.isHidden = true;
        if (this.children && this.children.length) {
            this.children.forEach((child: SelectorItemModel) => {
                child.hideToBottom();
            });
        }
    }

    /**
     * Shows this item and all parents (recursively)
     */
    showToUp() {
        this.isHidden = false;
        if (this.parent) {
            this.parent.showToUp();
        }
    }
}

/**
 * Model for data of one selector (for all types of selectors).
 * It contains set of SelectorItemModel (one selector's item)
 * and some methods for work with selector's data.
 * This model doesn't know how to show selector, it contains only data!
 */
export class SelectorModel {
    key: string;
    name: string;
    order: number;
    icon: string;
    placeholder: string;
    multiple: boolean;
    type: string; // flat | hierarchical | region
    disabled: boolean;

    items: {[item_id: string]: SelectorItemModel};

    flatListItems: Array<string> = null;

    selected: Array<string> = []; // SelectorItemModel

    rootItems: Array<string> = [];

    constructor() {
    }

    /**
     * Recreates storage (with hierarchy) of all selector's items,
     * deselects all previously selected items
     * @param items Array<SelectorItemInput>
     */
    setData(items: Array<SelectorItemInput>): void {
        this.deselect(this.selected);

        let rels = {};
        this.items = {};
        this.rootItems = [];

        // fill items storage
        for (let i = 0; i < items.length; i++) {
            let id = items[i]['id'].toString();
            let item = new SelectorItemModel(id, items[i]['name'],
                items[i]['icon'], items[i]['disabled']);
            this.items[id] = item;
            if (items[i]['parent_id']) {
                rels[id] = items[i]['parent_id'].toString();
            } else {
                this.rootItems.push(id);
            }
        }

        // set relations between items
        let keys = Object.keys(rels);
        for (let i = 0; i < keys.length; i++) {
            let id = keys[i];
            let parent_id = rels[id];
            this.items[id].addParent(this.items[parent_id]);
        }

        this.flatListItems = this.getFlat(this.getFirstLevelItems());
    }

    /**
     * Selects all items by passed id, (!)deselects all others
     * @param ids Array<string>
     */
    forceSelect(ids: Array<string>): void {
        let toSelect = ids.filter((id) => {
            return !!(this.selected.indexOf(id) == -1);
        }, this);
        let toDeselect = this.selected.filter((id) => {
            return !!(ids.indexOf(id) == -1);
        }, this);

        this.select(toSelect);
        this.deselect(toDeselect);
        this.fixSelection();
    }

    /**
     * Selects all passed items (match by id). Previous selection stays.
     * @param ids Array<string>
     */
    select(ids: Array<string>): void {
        if (!this.multiple) {
            this.deselect(this.selected);
        }
        for (let i=0;i<ids.length;i++) {
            try {
                if (this.selected.indexOf(ids[i]) == -1) {
                    this.items[ids[i]].isSelected = true;
                    this.selected.push(ids[i]);
                }
            } catch(e) {}
        }
    }

    /**
     * Deselects all passed items, remove this items from this.selected too
     * @param src_ids Array<string>
     */
    deselect(src_ids: Array<string>): void {
        let ids = src_ids.map((id) => { return id; });
        for (let i=0;i<ids.length; i++) {
            try {
                let index = this.selected.indexOf(ids[i]);
                if (index != -1) {
                    this.items[ids[i]].isSelected = false;
                    this.selected.splice(index, 1);
                }
            } catch(e) {}
        }
    }

    /**
     * Returns all root (first level) items
     * @returns {SelectorItemModel[]}
     */
    getFirstLevelItems(): SelectorItemModel[] {
        return this.rootItems.map((id) => {
            return this.items[id];
        }, this);
    }

    /**
     * Returns all selected items (as SelectorItemModel) in flat list
     * @returns {SelectorItemModel[]>}
     */
    getSelectedItems(): SelectorItemModel[] {
        return this.selected.map((id) => {
            return this.items[id];
        }, this);
    }

    /**
     * Returns all items (as SelectorItemModel) in flat list
     * @returns {SelectorItemModel[]}
     */
    getFlatListItems(): SelectorItemModel[] {
        return this.flatListItems.map((id) => {
            return this.items[id];
        }, this);
    }

    /**
     * Removes from selection non-existed items
     */
    private fixSelection() {
        this.selected = this.selected.filter((id) => {
            return !!(this.items[id]);
        }, this);
        if (!this.multiple && this.selected.length > 1) {
            let toDeselect = this.selected.slice(1, this.selected.length);
            this.deselect(toDeselect);
        }
    }

    /**
     * Returns hierarchical items as flat list of strings
     * @param inputList Array<SelectorItemModel>
     * @returns {Array<string>}
     */
    private getFlat(inputList: Array<SelectorItemModel>) : Array<string> {
        let outputList: Array<string> = [];
        for (let i = 0; i < inputList.length; i++) {
            if (inputList[i]) {
                outputList.push(inputList[i].id);
                if (inputList[i].children && inputList[i].children.length > 0){
                    let children = this.getFlat(inputList[i].children);
                    // console.log(children);
                    if (children && children.length) {
                        outputList = outputList.concat(children);
                    }
                }
            }
        }
        return outputList;
    }
}
