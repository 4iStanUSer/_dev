export interface SelectorItemInput {
    name: string;
    id: number|string;
    parent_id: number|string;
}
export interface SelectorConfigInput {
    name: string;
    placeholder: string;
    multiple: boolean;
    type: string; // flat | hierarchical | region
    icon: string;
    disabled?: boolean;
}

export class SelectorItemModel {
    id: string = null; //number|
    name: string = null;
    isSelected: boolean = false;
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

    addParent(parent: SelectorItemModel) {
        this.parent = parent;
        this.parent.children.push(this);
    }
}
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

    selected: Array<string> = []; // SelectorItemModel

    rootItems: Array<string> = [];

    constructor() {
    }

    setData(items: Array<SelectorItemInput>): void {
        let rels = {};
        this.items = {};
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
    }

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

    private fixSelection() {
        this.selected = this.selected.filter((id) => {
            return !!(this.items[id]);
        }, this);
        if (!this.multiple && this.selected.length > 1) {
            let toDeselect = this.selected.slice(1, this.selected.length);
            this.deselect(toDeselect);
        }
    }

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

    deselect(ids: Array<string>): void {
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

    getFirstLevelItems(): Array<SelectorItemModel> {
        return this.rootItems.map((id) => {
            return this.items[id];
        }, this);
    }

    getSelectedItems(): Array<SelectorItemModel> {
        return this.selected.map((id) => {
            return this.items[id];
        }, this);
    }
}
