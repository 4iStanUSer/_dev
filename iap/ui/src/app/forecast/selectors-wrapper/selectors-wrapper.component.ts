import { Component, OnInit } from '@angular/core';
import {AjaxService} from "../../common/service/ajax.service";

// import {SelectorConfigInput} from "../selectors/selector.model";
//import {SelectorModel} from "../selectors/selector.model";

// import {
//     SelectorConfigInput
// } from "./selectors/selector.model";


// interface SelectorConfigInput {
//     name: string;
//     placeholder: string;
//     multiple: boolean;
//     type: string; // flat | hierarchical | region
//     icon: string;
//     disabled?: boolean;
// }
//
// interface SelectorsConfigInput {
//     selectors: {[selectorKey: string]: SelectorConfigInput};
//     order: Array<string>;
// }

@Component({
  selector: 'selectors-wrapper',
  templateUrl: './selectors-wrapper.component.html',
  styleUrls: ['./selectors-wrapper.component.css']
})
export class SelectorsWrapperComponent implements OnInit {

    public wConfigObject: Object = null;
    public wDefaultSelection: Object = null;
    public isExpanded: boolean = false;
    public clickedTab:string = null;
    public currentSelection: Object = null;

    constructor() {}

    ngOnInit() {
        //console.log("selectors-wrapper init started");
        this.getConfig();
        this.getDefaultSelection();
        this.currentSelection = this.wDefaultSelection;
        //console.log("this.currentSelection", this.currentSelection);
        //console.log("selectors-wrapper init ended");
    }
    getConfig() {
        let mockConfigObject = {
            'order': ["geography", "products", "market"],
            'selectors': {
                'geography': {
                    'disabled':false,
                    'icon':"location",
                    'multiple':"1",
                    'name':"geography",
                    'placeholder':"geography",
                    'type':"hierarchical"
                },
                'market': {
                    'disabled':false,
                    'icon':"location",
                    'multiple':"1",
                    'name':"market",
                    'placeholder':"market",
                    'type':"hierarchical"
                },
                'products': {
                    'disabled':false,
                    'icon':"location",
                    'multiple':"1",
                    'name':"products",
                    'placeholder':"products",
                    'type':"hierarchical"
                }
            }
        };
        this.wConfigObject = mockConfigObject;
    }

    getDefaultSelection(){
        let mockDefaultSelection = {
            'geography': ["canada", "italy"],
            'market': ["all"],
            'products': ["mouthwash"]
        }
        this.wDefaultSelection = mockDefaultSelection;
    }

    private showPopUpClick(key: string, e: MouseEvent) {
        e.preventDefault();
        this.isExpanded = true;
        this.clickedTab = key;
    }

    onApplyClick(currentSelection:Object = null){
        //send currentSelection to server
        //console.log('wrapper onApplyClick', currentSelection);
        this.currentSelection = currentSelection;
        this.isExpanded = false;
        //console.log("this.currentSelection", this.currentSelection);
    }

    onCancelClick() {
        this.isExpanded = false;
        this.currentSelection = this.wDefaultSelection;
    }
}
