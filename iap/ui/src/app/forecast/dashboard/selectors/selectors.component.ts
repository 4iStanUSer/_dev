import {
    Component,
    Input,
    Output,
    OnInit,
    OnChanges,
    SimpleChanges,
    EventEmitter
} from '@angular/core';
import {
    SelectorItemInput, SelectorModel, SelectorConfigInput, SelectorItemModel
} from "./../../../common/model/selector.model";

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
export class SelectorsComponent implements OnInit, OnChanges {

    @Input() data: SelectorsDataInput;
    @Input() config: SelectorsConfigInput;

    @Output() changed: EventEmitter<SelectorsChangedOutput> = new EventEmitter();

    private selectors: Array<{
        model: SelectorModel,
        selected: Array<SelectorItemModel>
    }> = [];

    private state: Object = {
        isExpanded: false,
        activeTab: 0
    };

    constructor() {
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        console.info('SelectorsComponent -> ngOnChanges()');

        // if (ch['config']) {
        // // TODO Implement Reconfiguring procedure (VL)
        // }

        if (ch['data']) {
            this.selectors = []; // TODO Implement not recreation but updating (Vl)

            let order = this.config['order'];
            for (let i = 0; i < order.length; i++) { // TODO Maybe move procedure of creating to config section
                let selKey = order[i];
                try {
                    let config = this.config['selectors'][selKey];
                    let data = ch['data']['currentValue'][selKey]['data'];
                    let selected = ch['data']['currentValue'][selKey]['selected'];
                    // TODO Implement (VL)

                    let model = new SelectorModel();
                    model.order = i;
                    model.key = selKey;

                    // Configuring model from config object
                    model.name = config['name'];
                    model.placeholder = config['placeholder'];
                    model.multiple = config['multiple'];
                    model.type = config['type'];
                    model.icon = config['icon'];
                    model.disabled = !!config['disabled'];
                    // .Configuring model from config object

                    model.setData(data);
                    model.forceSelect(selected);

                    let sel = model.getSelectedItems();
                    this.selectors.push({
                        model: model,
                        selected: sel,
                    });

                } catch (e) {
                    console.error('Error - ' + e.toString());
                }
            }
        }
    }

    private onPreviewClick(index: number, e: MouseEvent) {
        e.preventDefault();
        this.setActiveTab(index);
        this.state['isExpanded'] = true;

    }

    private setActiveTab(index: number) {
        this.state['activeTab'] = index;
    }

    private onApplyClick() {
        this.state['isExpanded'] = false;
        let changed = false;
        let output = {};
        for (let i=0;i<this.selectors.length;i++) {
            let changedThis = false;
            let currSelected = this.selectors[i]['model'].getSelectedItems();
            if (currSelected.length != this.selectors[i]['selected'].length) {
                changed = true;
                changedThis = true;
            } else {
                let diff = currSelected.filter((item) => {
                    return (this.selectors[i]['selected'].indexOf(item) == -1);
                }, this);
                if (diff.length > 0) {
                    changed = true;
                    changedThis = true;
                }
            }
            if (changedThis) {
                this.selectors[i]['selected'] = currSelected;
            }

            output[this.selectors[i].model.key] =
                this.selectors[i]['selected'].map((item) => {
                    return item['id'];
                });
        }
        if (changed) {
            console.log('-->SELECTORS changed', output);
            this.changed.emit(output);
        }
    }

    private onCancelClick() {
        this.state['isExpanded'] = false;

        this.selectors.forEach((selector) => {
            let sel = selector['selected'].map((item) => {
                return item.id;
            });
            selector['model'].forceSelect(sel);
        });
    }

}
