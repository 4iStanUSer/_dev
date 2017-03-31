import {
    Component,
    Output,
    OnInit,
    Input,
    EventEmitter,
    SimpleChanges,
    OnChanges,
} from '@angular/core';
import {
    SelectorItemInput, SelectorModel, SelectorConfigInput, SelectorItemModel
} from "./selector.model";
import {AjaxService} from "../../common/service/ajax.service";
import {StaticConfigModel} from "./static.config.model";

/*
 * Notice-Requirements:*
 * 1. Flat structure for any input data
 * 2. For Configuration we use any that is needed for initial instantiation
 * of selector, such as placeholder, name, type ...
 * */

interface SelectorsListInput{
    [selectorKey: string]:
        Array<SelectorItemInput>
    ;
}

interface SelectionInput {
    [selectorKey: string]:
        Array<string>
    ;
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


    @Input() configObject: SelectorsConfigInput;
    @Input() defaultSelection: SelectionInput;
    @Input() tabToActivate: string = "";

    private deactivate:boolean = false;

    private configured: boolean = false;

    private staticConfig: StaticConfigModel = this.setStaticConfig(new StaticConfigModel());

    private config: SelectorsConfigInput = null;


    @Output() changed = new EventEmitter();

    private selectors: {
        [selector_key: string]: {
            model: SelectorModel,
            selected: Array<SelectorItemModel>
        }
    } = {};
    private selectorsOrder: Array<string> = [];

    private state: Object = {
        //isExpanded: false,
        activeTab: null
    };

    constructor(private req: AjaxService) {
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['tabToActivate']) {
            //console.log('ngOnChanges',this.tabToActivate);
            this.setActiveTab(this.tabToActivate);
        }
    }

    ngOnInit() {
        //console.log('selectors init started');
        this.setConfiguration(this.configObject);
        this.initSelectorsList();
        this.initSelection();
        //console.log('selectors init ended');
    }

    private setStaticConfig(staticConfig:StaticConfigModel){
        //request to get static data
        this.req.post({
            url_id: 'forecast/get_selectors_static_config',
            data: {}
        }).subscribe((data) => {
            Object.assign(staticConfig['fields'], data);
                return staticConfig;
        });
        return staticConfig;
    }

    setConfiguration(c: SelectorsConfigInput) {
        this.config = c;
        this.selectors = {};
        this.selectorsOrder = [];

        let order = this.config['order'];

        if (this.config['order'].length > 0) {
            if (!this.state['activeTab']){
                this.state['activeTab'] = this.config['order'][0];
            }
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

                    model.staticConfig = this.staticConfig;

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
        //console.log('setConfiguration model end', this.selectors);
        this.configured = true;
    }

    initSelectorsList(){
        let mockSelectorsList = {
            'geography': [
                {'id': "canada", 'parent_id': null, 'name': "canada", 'disabled': false, 'icon': ""},
                {'id': "italy", 'parent_id': null, 'name': "italy", 'disabled': false, 'icon': ""},
                {'id': "germany", 'parent_id': null, 'name': "germany", 'disabled': false, 'icon': ""},
                {'id': "uk", 'parent_id': null, 'name': "uk", 'disabled': false, 'icon': ""},
                {'id': "us", 'parent_id': null, 'name': "us", 'disabled': false, 'icon': ""},
                {'id': "brazil", 'parent_id': null, 'name': "brazil", 'disabled': false, 'icon': ""},
                {'id': "australia", 'parent_id': null, 'name': "australia", 'disabled': false, 'icon': ""},
                {'id': "japan", 'parent_id': null, 'name': "japan", 'disabled': false, 'icon': ""},
                {'id': "spain", 'parent_id': null, 'name': "spain", 'disabled': false, 'icon': ""},
                {'id': "mexico", 'parent_id': null, 'name': "mexico", 'disabled': false, 'icon': ""},
                {'id': "all", 'parent_id': null, 'name': "all", 'disabled': false, 'icon': ""}
            ],
            'market': [
                {'id': "all", 'parent_id': null, 'name': "all", 'disabled': false, 'icon': ""}
            ],
            'products': [
                {'id': "mouthwash", 'parent_id': null, 'name': "mouthwash", 'disabled': false, 'icon': ""},
                {'id': "all", 'parent_id': null, 'name': "all", 'disabled': false, 'icon': ""}
            ]
        }
        this.setSelectorsList(mockSelectorsList);
    }

    updateSelectorsList(selected:SelectionInput){
        let mockSelectorsList = {
            'geography': [
                {'id': "canada", 'parent_id': null, 'name': "canada", 'disabled': false, 'icon': ""},
                {'id': "italy", 'parent_id': null, 'name': "italy", 'disabled': false, 'icon': ""},
                {'id': "germany", 'parent_id': null, 'name': "germany", 'disabled': false, 'icon': ""},
                {'id': "uk", 'parent_id': null, 'name': "uk", 'disabled': false, 'icon': ""},
                {'id': "us", 'parent_id': null, 'name': "us", 'disabled': false, 'icon': ""},
                {'id': "brazil", 'parent_id': null, 'name': "brazil", 'disabled': false, 'icon': ""}
            ],
            'market': [
                {'id': "all", 'parent_id': null, 'name': "all", 'disabled': false, 'icon': ""}
            ],
            'products': [
                {'id': "mouthwash", 'parent_id': null, 'name': "mouthwash", 'disabled': false, 'icon': ""},
                {'id': "cars", 'parent_id': null, 'name': "cars", 'disabled': false, 'icon': ""},
                {'id': "all", 'parent_id': null, 'name': "all", 'disabled': false, 'icon': ""}
            ]
        }
        this.setSelectorsList(mockSelectorsList);
    }

    setSelectorsList(sl:SelectorsListInput){
        if (this.configured) {
            for (let i = 0; i < this.selectorsOrder.length; i++) {
                try {
                    let selKey = this.selectorsOrder[i];
                    if (sl[selKey]) { // Update Logic
                        let data = sl[selKey];
                        this.selectors[selKey].model.setData(data);
                    }
                } catch (e) {
                    //  TODO Fatal Error - Can't work
                    console.error('Fatal Error - ' + e.toString());
                }
            }
        } else {
            //this.data = d;
            console.error('selectors configuration is not set yet');
        }
    }

    initSelection(){
        // console.log('this.defaultSelection in get');
        // console.log(this.defaultSelection);
        this.setSelection(this.defaultSelection);
    }

    updateSelection(){
        let mockSelection = {
                'geography': ["canada", "italy"],
                'market': ["all"],
                'products': ["all"]
            }
        this.setSelection(mockSelection);
    }

    setSelection(s:SelectionInput){
        //console.log("setSelection");
        if (this.configured) {
            //console.log("setSelection this.configured");
            for (let i = 0; i < this.selectorsOrder.length; i++) {
                try {
                    let selKey = this.selectorsOrder[i];
                    if (s[selKey]) { // Update Logic

                        let selected = s[selKey];
                        //console.log("setSelection selected", selected);
                        this.selectors[selKey].model.forceSelect(selected);

                        let sel = this.selectors[selKey].model
                            .getSelectedItems();
                        this.selectors[selKey].selected = sel;
                    }
                } catch (e) {
                    //  TODO Fatal Error - Can't work
                    console.error('Fatal Error - ' + e.toString());
                }
            }
        } else {
            console.error('selectors configuration is not set yet');
        }
    }

    private onPreviewClick(key: string, e: MouseEvent) {
        e.preventDefault();
        this.setActiveTab(key);
        //this.state['isExpanded'] = true;
        this.updateInputsOnTabChange();
    }

    /**
     * Sets active tab by passed key - string id
     */
    private setActiveTab(key: string) {
        //console.log("setActiveTab", key);
        this.state['activeTab'] = key;
    }

    //updateInputsOnTabChange
    private updateInputsOnTabChange(){
        let userSelection = this.getSelection();
        this.updateSelectorsList(userSelection);
        this.updateSelection();
    }

    /**
     * Returns current selection
     */
    private getSelection(): SelectionInput{
        let output = {};
        for (let i = 0; i < this.selectorsOrder.length; i++) {
            let selKey = this.selectorsOrder[i];
            let currSelected = this.selectors[selKey]['model']
                .getSelectedItems();
            // console.log("currSelected", i, "");
            // console.log(currSelected);

            output[this.selectors[selKey].model.key] =
                currSelected.map((item) => {
                    return item['id'];
                });
        }
        //console.log("getSelection output", output);
        return output;
    }

    private onNothingSelected(nothingSelected:boolean){
        //console.log("onSelectionChange",nothingSelected);
        this.deactivate = nothingSelected;
    }



    //*********not used anymore

    // interface SelectorsDataInput {
    //     [selectorKey: string]: {
    //         data: Array<SelectorItemInput>,
    //         selected: Array<number|string>
    //     };
    // }
    //
    // private hasData: boolean = false;
    //private data: SelectorsDataInput = null;

    // private onApplyClick() {
    //     //this.state['isExpanded'] = false;
    //     let changed = false;
    //     let output = {};
    //     for (let i = 0; i < this.selectorsOrder.length; i++) {
    //         let selKey = this.selectorsOrder[i];
    //         let changedThis = false;
    //         let currSelected = this.selectors[selKey]['model']
    //             .getSelectedItems();
    //         if (currSelected.length !=
    //             this.selectors[selKey]['selected'].length) {
    //             changed = true;
    //             changedThis = true;
    //         } else {
    //             let diff = currSelected.filter((item) => {
    //                 return (this.selectors[selKey]['selected']
    //                     .indexOf(item) == -1);
    //             }, this);
    //             if (diff.length > 0) {
    //                 changed = true;
    //                 changedThis = true;
    //             }
    //         }
    //         if (changedThis) {
    //             this.selectors[selKey]['selected'] = currSelected;
    //         }
    //
    //         output[this.selectors[selKey].model.key] =
    //             this.selectors[selKey]['selected'].map((item) => {
    //                 return item['id'];
    //             });
    //     }
    //     if (changed) {
    //         //console.log('-->SELECTORS changed', output);
    //         this.setData(output);// TO DO Test reselecting
    //     }
    // }

    // private onCancelClick() {
    //     //this.state['isExpanded'] = false;
    //
    //     this.selectorsOrder.forEach((selKey) => {
    //         let sel = this.selectors[selKey]['selected'].map((item) => {
    //             return item.id;
    //         });
    //         this.selectors[selKey]['model'].forceSelect(sel);
    //     }, this);
    // }

    // private setModeDetails(){
    //     this.setActiveTab("geography");
    //     //this.state['isExpanded'] = true;
    //
    //     // this.setActiveTab(key);
    //     // this.state['isExpanded'] = true;
    //     //this.changeTabDataUpdate();
    // }

    // getConfig() {
    //     console.log("selectors getConfig started");
    //     this.req.post({
    //         url_id: 'forecast/get_entity_selectors_config',
    //         data: {}
    //     }).subscribe((data) => {
    //         this.initConfig(data);
    //         console.log("selectors DATA CAME");
    //         console.log(data);
    //     });
    //     console.log("selectors getConfig ended");
    // }

    // setData(query: { [selector_id: string]: Array<string>} = null) {
    //     this.req.post({
    //         url_id: 'forecast/set_entity_selection',
    //         data: {
    //             query: query
    //         }
    //     }).subscribe((data) => {
    //         console.log('data sent');
    //         this.changed.emit();
    //         this.initData(data);
    //     });
    // }

    //
    // private updateInputsOnTabChange(){
    //     let changed = false;
    //     let output = {};
    //     for (let i = 0; i < this.selectorsOrder.length; i++) {
    //         let selKey = this.selectorsOrder[i];
    //         let changedThis = false;
    //         let currSelected = this.selectors[selKey]['model']
    //             .getSelectedItems();
    //         if (currSelected.length !=
    //             this.selectors[selKey]['selected'].length) {
    //             changed = true;
    //             changedThis = true;
    //         } else {
    //             let diff = currSelected.filter((item) => {
    //                 return (this.selectors[selKey]['selected']
    //                     .indexOf(item) == -1);
    //             }, this);
    //             if (diff.length > 0) {
    //                 changed = true;
    //                 changedThis = true;
    //             }
    //         }
    //         if (changedThis) {
    //             this.selectors[selKey]['selected'] = currSelected;
    //         }
    //
    //         output[this.selectors[selKey].model.key] =
    //             this.selectors[selKey]['selected'].map((item) => {
    //                 return item['id'];
    //             });
    //     }
    //     if (changed) {
    //         //console.log('-->SELECTORS changed', output);
    //         //this.setData(output);
    //         this.getData(output);
    //     }
    // }

    // getData(query: { [selector_id: string]: Array<string>} = null) {
    //     this.req.post({
    //         url_id: 'forecast/get_options_for_entity_selector',
    //         data: {
    //             query: query
    //         }
    //     }).subscribe((data) => {
    //         console.log('received options');
    //         this.initData(data);
    //     });
    // }

    // initData(d) {
    //     //console.log("initDATA in SelectorsComponent");
    //     if (this.configured) {
    //         for (let i = 0; i < this.selectorsOrder.length; i++) {
    //             try {
    //                 let selKey = this.selectorsOrder[i];
    //                 if (d[selKey] && d[selKey]['data']) { // Update Logic
    //                     let data = d[selKey]['data'];
    //                     this.selectors[selKey].model.setData(data);
    //                 }
    //                 if (d[selKey] && d[selKey]['selected']) { // Update Logic
    //                     let selected = d[selKey]['selected'];
    //                     this.selectors[selKey].model.forceSelect(selected);
    //
    //                     let sel = this.selectors[selKey].model
    //                         .getSelectedItems();
    //                     this.selectors[selKey].selected = sel;
    //                 } else {
    //                     // TO DO Maybe deselect all
    //                 }
    //             } catch (e) {
    //                 //  TO DO Fatal Error - Can't work
    //                 console.error('Fatal Error - ' + e.toString());
    //             }
    //         }
    //     } else {
    //         this.data = d;
    //     }
    //     this.hasData = true;
    // }
}
