import {
    Component,
    Input,
    OnInit,
    OnChanges,
    SimpleChanges
} from '@angular/core';

/*
 * Notice-Requirements:*
 * 1. Flat structure for any input data
 * 2. For Configuration we use any that is needed for initial instantiation
 * of selector, such as placeholder, name, type ...
 * */


interface SelectorsDataInput {
    [selectorKey: string]: {
        data: Array<{
            label: string,
            id: number|string,
            parent_id: number|string
        }>,
        selected: Array<number|string>
    };
}
interface SelectorsConfigInput {
    selectors: {[selectorKey: string]: {
        name: string;
        placeholder: string;
        multiple: boolean;
        type: string; // flat | hierarchical | region
        icon: string;
        disabled?: boolean;
    }};
    order: Array<string>;
}

////////////////////////////////////////////////////////////

class SelectorItemModel {
    id: number|string = null;
    label: string = null;
    isSelected: boolean = false;
    icon?: string = null;
    disabled?: boolean = false;

    parent: SelectorItemModel = null;
    children: Array<SelectorItemModel> = [];
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

    items: Array<SelectorItemModel>;

    constructor() {
    }
}

@Component({
    selector: 'selectors',
    templateUrl: './selectors.component.html',
    styleUrls: ['./selectors.component.css']
})
export class SelectorsComponent implements OnInit, OnChanges {

    @Input() data: SelectorsDataInput;
    @Input() config: SelectorsConfigInput;

    // private selectors: {
    //     [selector: string]: {
    //         model: SelectorModel,
    //         // TODO Add more (VL)
    //     }
    // } = null;

    private selectors: Array<{
        model: SelectorModel,
        // TODO Add more (VL)
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

                    // this.selectors[selKey] = {
                    //     model: model
                    // };
                    this.selectors.push({
                        model: model
                    })
                } catch (e) {
                    console.error('Error - ' + e.toString());
                }
            }

            console.log(this.selectors);
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


}
