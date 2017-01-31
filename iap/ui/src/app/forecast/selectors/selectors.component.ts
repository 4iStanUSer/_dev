import {
    Component,
    Output,
    OnInit,
    EventEmitter
} from '@angular/core';
import {
    SelectorItemInput, SelectorModel, SelectorConfigInput, SelectorItemModel
} from "./selector.model";
import {AjaxService} from "../../common/service/ajax.service";

/*
 * Notice-Requirements:*
 * 1. Flat structure for any input data
 * 2. For Configuration we use any that is needed for initial instantiation
 * of selector, such as placeholder, name, type ...
 * */


interface SelectorsDataInput {
    [selectorKey: string]: {
        data: Array<SelectorItemInput>,
        selected: Array<number|string>
    };
}
interface SelectorsConfigInput {
    selectors: {[selectorKey: string]: SelectorConfigInput};
    order: Array<string>;
}

interface SelectorsChangedOutput {
    [selectorKey: string]: Array<string>
}


@Component({
    selector: 'selectors',
    templateUrl: './selectors.component.html',
    styleUrls: ['./selectors.component.css']
})
export class SelectorsComponent implements OnInit { //, OnChanges

    private configured: boolean = false;
    private hasData: boolean = false;

    private config: SelectorsConfigInput = null;
    private data: SelectorsDataInput = null;


    @Output() changed = new EventEmitter();

    private selectors: {
        [selector_key: string]: {
            model: SelectorModel,
            selected: Array<SelectorItemModel>
        }
    } = {};
    private selectorsOrder: Array<string> = [];

    private state: Object = {
        isExpanded: false,
        activeTab: null
    };

    constructor(private req: AjaxService) {
    }

    ngOnInit() {

        this.getConfig();
        this.getData();
    }

    getConfig() {
        this.req.post({
            url_id: 'forecast/get_entity_selectors_config',
            data: {}
        }).subscribe((data) => {
            this.initConfig(data);
        });
    }

    getData(query: { [selector_id: string]: Array<string>} = null) {
        this.req.post({
            url_id: 'forecast/get_options_for_entity_selector',
            data: {
                query: query
            }
        }).subscribe((data) => {
            console.log('received options');
            this.initData(data);
        });
    }

    setData(query: { [selector_id: string]: Array<string>} = null) {
        this.req.post({
            url_id: 'forecast/set_entity_selection',
            data: {
                query: query
            }
        }).subscribe((data) => {
            console.log('data sent');
            this.changed.emit();
        });
    }

    initConfig(c: SelectorsConfigInput) {
        // TODO Implement procedure of reconfigure but not recreating
        this.config = c;
        this.selectors = {};
        this.selectorsOrder = [];

        let order = this.config['order'];

        if (this.config['order'].length > 0) {
            this.state['activeTab'] = this.config['order'][0];
            for (let i = 0; i < order.length; i++) {
                let selKey = order[i];
                try {
                    let config = this.config['selectors'][selKey];
                    let model = new SelectorModel();
                    model.order = i;
                    model.key = selKey;
                    model.name = config['name'];
                    model.placeholder = config['placeholder'];
                    model.multiple = config['multiple'];
                    model.type = config['type'];
                    model.icon = config['icon'];
                    model.disabled = !!config['disabled'];

                    this.selectors[selKey] = {
                        model: model,
                        selected: null,
                    };
                    this.selectorsOrder.push(selKey);

                } catch (e) {
                    console.error('Fatal Error - ' + e.toString());
                }
            }
        }

        this.configured = true;
        if (this.hasData) {
            this.initData(this.data);
        }
    }

    initData(d) {
        if (this.configured) {
            for (let i = 0; i < this.selectorsOrder.length; i++) {
                try {
                    let selKey = this.selectorsOrder[i];
                    if (d[selKey] && d[selKey]['data']) { // Update Logic
                        let data = d[selKey]['data'];
                        this.selectors[selKey].model.setData(data);
                    }
                    if (d[selKey] && d[selKey]['selected']) { // Update Logic
                        let selected = d[selKey]['selected'];
                        this.selectors[selKey].model.forceSelect(selected);

                        let sel = this.selectors[selKey].model
                            .getSelectedItems();
                        this.selectors[selKey].selected = sel;
                    } else {
                        // TODO Maybe deselect all
                    }
                } catch (e) {
                    //  TODO Fatal Error - Can't work
                    console.error('Fatal Error - ' + e.toString());
                }
            }
        } else {
            this.data = d;
        }
        this.hasData = true;
    }

    private onPreviewClick(key: string, e: MouseEvent) {
        e.preventDefault();
        this.setActiveTab(key);
        this.state['isExpanded'] = true;
    }

    private setActiveTab(key: string) {
        this.state['activeTab'] = key;
    }

    private onApplyClick() {
        this.state['isExpanded'] = false;
        let changed = false;
        let output = {};
        for (let i = 0; i < this.selectorsOrder.length; i++) {
            let selKey = this.selectorsOrder[i];
            let changedThis = false;
            let currSelected = this.selectors[selKey]['model']
                .getSelectedItems();
            if (currSelected.length !=
                this.selectors[selKey]['selected'].length) {
                changed = true;
                changedThis = true;
            } else {
                let diff = currSelected.filter((item) => {
                    return (this.selectors[selKey]['selected']
                        .indexOf(item) == -1);
                }, this);
                if (diff.length > 0) {
                    changed = true;
                    changedThis = true;
                }
            }
            if (changedThis) {
                this.selectors[selKey]['selected'] = currSelected;
            }

            output[this.selectors[selKey].model.key] =
                this.selectors[selKey]['selected'].map((item) => {
                    return item['id'];
                });
        }
        if (changed) {
            console.log('-->SELECTORS changed', output);
            this.setData(output);// TODO Test reselecting
        }
    }

    private onCancelClick() {
        this.state['isExpanded'] = false;

        this.selectorsOrder.forEach((selKey) => {
            let sel = this.selectors[selKey]['selected'].map((item) => {
                return item.id;
            });
            this.selectors[selKey]['model'].forceSelect(sel);
        }, this);
    }
}
