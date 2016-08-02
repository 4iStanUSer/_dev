import {
    Component,
    ViewChild,
    ViewContainerRef,
} from '@angular/core';

import { ComponentFactoryService } from './../../common/service/component-factory.service';
import { TimeseriesWidgetComponent } from './../../common/cmp/timeseries-widget/';
import { HierarchyWidgetComponent } from './../../common/cmp/hierarchy-widget/';
import { DropdownComponent } from './../../common/cmp/dropdown/';
import { IndexPageService } from './../service/index-page.service';
import { DatepickerComponent } from "./../../common/cmp/datepicker/";

@Component({
    selector: 'navigation-panel',
    template: `<ng-content></ng-content>`
})
export class NavagationPanelComponent { }


// TODO move to common part
interface IWidget {
    name: string;
    widget: string; // 'hierarchy', 'dropdown', 'datepicker' ...
    data: any;
    component?: any;
}
// class ZoneOptions {
//     name: string = null;
//     widget: string = null; // 'grid' ...
//     data: Object = null;
// }
interface INavPanelOptions {
    order: Array<string>;
    dimensions: Array<IWidget>;
}
class ContentOptions {
    order: Array<string>;
    zones: Array<IWidget>;
}
interface IPageData {
    nav_panel: INavPanelOptions;
    content: ContentOptions;
}


// <!--
//         <dropdown [items]="__DROPDOWN_ITEMS" [configuration]="__DROPDOWN_CONFIG" (changeSelection)="dropdownSelectionChanged($event)"></dropdown>
//
//         <hierarchy-widget [items]="__HIERARCHY_ITEMS" (itemSelected)="hierarchyItemSelect($event)"></hierarchy-widget>
//
//         <hierarchy-widget [items]="__HIERARCHY_ITEMS1" (itemSelected)="hierarchyItemSelect($event)"></hierarchy-widget>
//
//         <datepicker [date]="__CURRENT_DATE" (dateChanged)="dateChanged($event)"></datepicker>
// -->

@Component({
    moduleId: module.id,
    selector: 'forecast-index-page',
    directives: [
        TimeseriesWidgetComponent,
        HierarchyWidgetComponent,
        DropdownComponent,
        DatepickerComponent,

        NavagationPanelComponent
    ],
    providers: [IndexPageService],
    styles: [
        `#nav_panel {
background: #908c8c;
height:100%;
overflow-y:auto;
}`,
        `#cont_panel {
background: #cecece;
height:100%;
overflow-y:auto;
}`
    ],
    template: `
<div class="row">
    <navigation-panel class="col-sm-3">
        <div #navPanel></div>
    </navigation-panel>

    <div class="col-sm-9" id="cont_panel">
        <h1>main content</h1>
{{currentSelection | json}}
        <div #contentZone></div>

    </div>
</div>
`
})
export class IndexPageComponent {
    private pageData: any = null;// TODO via Interface IPageOptions

    private currentSelection = {};

    constructor(
        private pageService: IndexPageService,
        private cmpFactoryServ: ComponentFactoryService
    ) { }

    private updateDimensionsData(d){
        let block = null;
        let data = null;
        let name = null;
        let newData = null;
        for (let i=0; i<this.pageData.nav_panel.dimensions.length;i++){ //this.pageData.nav_panel.order
            block = this.pageData.nav_panel.dimensions[i];
            name = this.pageData.nav_panel.dimensions[i].name;
            newData = d.nav_panel.dimensions.filter(function(dim){
                return (dim.name == name) ? true : false;
            });
            data = (newData && newData[0]) ? newData[0].data : [];
            if (block['widget'] == 'hierarchy') {
                block.component['items'] = data;
            } else if (block['widget'] == 'dropdown') {
                block.component['items'] = data;
            }
        }
        for (let i=0; i<this.pageData.content.zones.length;i++){ //this.pageData.nav_panel.order
            block = this.pageData.content.zones[i];
            name = this.pageData.content.zones[i].name;
            newData = d.content.zones.filter(function(zone){
                return (zone.name == name) ? true : false;
            });
            data = (newData && newData[0]) ? newData[0].data : [];
            if (block['widget'] == 'timeseries') {
                block.component['timeseries'] = block.data;
            }
        }
    }
    private hierarchySelectionChanged(item: Object, name: string) {
        this.currentSelection[name] = item;

        this.pageService
            .get_index_page_data(this.currentSelection)
            .subscribe((d) => {
                this.updateDimensionsData(d);
            });
    }
    private dropdownSelectionChanged(item: Object, name: string) {
        this.currentSelection[name] = item;

        this.pageService
            .get_index_page_data(this.currentSelection)
            .subscribe((d) => {
                this.updateDimensionsData(d);
            });
    }
    public __DROPDOWN_CONFIG = {
        'multiple': false,
    };

    public __TIMESERIES: any = null; //Array<Object>
    public __HIERARCHY_ITEMS: any = null; //Array<Object>
    public __HIERARCHY_ITEMS1: any = null; //Array<Object>
    public __DROPDOWN_ITEMS: any = null; //Array<Object>

    // ngOnDestroy() { // TODO
    //     if(this.cmpRef)
    //         this.cmpRef.destroy();
    // }

    @ViewChild('navPanel', {read: ViewContainerRef}) navPanel;
    @ViewChild('contentZone', {read: ViewContainerRef}) contentZone;

    ngOnInit() {

        this.pageService
            .get_index_page_data(this.currentSelection)
            .subscribe((d) => {
                this.pageData = d; //IPageOptions
                if (this.pageData.nav_panel && this.pageData.nav_panel.dimensions) {
                    // clear navigation
                    let dimensions = this.pageData.nav_panel.dimensions; // Array<IWidget>
                    for (let i=0 ; i<dimensions.length; i++){
                        let block = dimensions[i];
                        this.currentSelection[block['name']] = null;
                        let cmp = this.cmpFactoryServ.generate(block['widget'], this.navPanel, this);
                        if (cmp) {
                            cmp.then((component) => {

                                this.pageData.nav_panel.dimensions[i].component = component;

                                let that = this;
                                if (block['widget'] == 'hierarchy') {
                                    component['currentSelection'].subscribe(function(event){
                                        console.log('currentSelection');
                                        that.currentSelection[block['name']] = event;
                                    });
                                    component['itemSelected'].subscribe(function(event){
                                        that.hierarchySelectionChanged(event, block['name']);
                                    });
                                    component['items'] = block.data;

                                } else if (block['widget'] == 'dropdown') {
                                    component['currentSelection'].subscribe(function(event){
                                        console.log('currentSelection');
                                        that.currentSelection[block['name']] = event;
                                    });
                                    component['changeSelection'].subscribe(function(event){
                                        that.dropdownSelectionChanged(event, block['name']);
                                    });
                                    component['items'] = block.data;
                                    component['configuration'] = that.__DROPDOWN_CONFIG;
                                }
                            });
                        }
                    }
                }

                if (this.pageData.content && this.pageData.content.zones) {
                    let zones = this.pageData.content.zones; // Array<IWidget>
                    for (let i=0 ; i<zones.length; i++){
                        let block = zones[i];

                        let cmp = this.cmpFactoryServ.generate(block['widget'], this.contentZone, this);
                        if (cmp) {
                            cmp.then((component) => {

                                this.pageData.content.zones[i].component = component;

                                if (block['widget'] == 'timeseries') {
                                    component['timeseries'] = block.data;
                                }
                            });
                        }
                    }
                }
            });
    }

    /***********DatePicker*************/
    private __CURRENT_DATE = '25/07/2016';

    private dateChanged(new_date){
        console.log(new_date);
    }
    /***********.DatePicker*************/

    /***********DROPDOWN*************/

    // public __DROPDOWN_ITEMS: Array<Object> = [
    //     {
    //         "id": 27524, "text": "First variant",
    //         "state": {
    //             "disabled": false,
    //             "selected": false
    //         },
    //     },
    //     {
    //         "id": 27525, "text": "ss1",
    //         "state": {
    //             "disabled": true,
    //             "selected": false
    //         },
    //     },
    //     {
    //         "id": 27526, "text": "ss2",
    //         "state": {
    //             "disabled": false,
    //             "selected": false
    //         },
    //     },
    //     {
    //         "id": 27527, "text": "dd",
    //         "state": {
    //             "disabled": false,
    //             "selected": false
    //         },
    //     },
    //     {
    //         "id": 27530, "text": "Some another",
    //         "state": {
    //             "disabled": false,
    //             "selected": true
    //         },
    //     },
    // ];
    /***********DROPDOWN*************/
    /***********TIMESERIES*************/
    // public __TIMESERIES: Array<Object> = [
    //     {
    //         head: [
    //             {
    //                 value: 'Population',
    //                 meta: 'Variable'
    //             },
    //             {
    //                 value: 'Billion',
    //                 meta: 'Metric'
    //             }
    //         ],
    //         cells: [
    //             {
    //                 value: 123,
    //                 valueType: 'int',
    //                 meta: 'April'
    //             },
    //             {
    //                 value: 124,
    //                 valueType: 'int',
    //                 meta: 'May'
    //             },
    //             {
    //                 value: 125,
    //                 valueType: 'int',
    //                 meta: 'June'
    //             },
    //             {
    //                 value: 126,
    //                 valueType: 'int',
    //                 meta: 'July'
    //             }
    //         ],
    //         options: {}
    //     },
    //     {
    //         head: [
    //             {
    //                 value: 'GDP',
    //                 meta: 'Variable'
    //             },
    //             {
    //                 value: '$',
    //                 meta: 'Metric'
    //             }
    //         ],
    //         cells: [
    //             {
    //                 value: 1230,
    //                 valueType: 'int',
    //                 meta: 'April'
    //             },
    //             {
    //                 value: 1240,
    //                 valueType: 'int',
    //                 meta: 'May'
    //             },
    //             {
    //                 value: 1250,
    //                 valueType: 'int',
    //                 meta: 'June'
    //             },
    //             {
    //                 value: 1260,
    //                 valueType: 'int',
    //                 meta: 'July'
    //             }
    //         ],
    //         options: {}
    //     }
    // ]
    public __TIMESERIES_OPT = {}

    /***********.TIMESERIES*************/

    /***********HIERARCHY_WIDGET*************/

    // public __HIERARCHY_ITEMS: Array<Object> = [
    //     {
    //         "id": 27536, "text": "New node", "type": "parent",
    //         "state": {
    //             "opened": true,
    //             "disabled": false,
    //             "selected": true
    //         },
    //         "children": [
    //             { "id": 27524, "text": "ss", "type": "parent", "children": false },
    //             { "id": 27521, "text": "ss", "type": "child", "children": false }
    //         ]
    //     },
    //     {
    //         "id": 27529, "text": "New node", "type": "parent", "children": false
    //     },
    //     {
    //         "id": 27532, "text": "New node", "type": "child",
    //         "state": {
    //             "opened": false,
    //             "disabled": true,
    //             "selected": false
    //         },
    //         "children": false
    //     },
    //     {
    //         "id": 27538, "text": "New node", "type": "parent",
    //         "state": {
    //             "opened": false,
    //             "disabled": false,
    //             "selected": false
    //         },
    //         "children": [
    //             { "id": 7524, "text": "ss", "type": "parent", "children": false },
    //             { "id": 7521, "text": "ss", "type": "child", "children": false }
    //         ]
    //     }
    // ];
    // public __HIERARCHY_ITEMS1 = [
    //     {
    //         id: 1, text: 'root1',
    //         "state": {
    //             "opened": false,
    //             "disabled": false,
    //             "selected": false
    //         },
    //         children: [
    //             {
    //                 id: 2,
    //                 text: 'child1',
    //                 "state": {
    //                     "opened": false,
    //                     "disabled": false,
    //                     "selected": true
    //                 },
    //             }, {
    //                 id: 3,
    //                 text: 'child2',
    //                 "state": {
    //                     "opened": false,
    //                     "disabled": false,
    //                     "selected": false
    //                 },
    //             }
    //         ]
    //     },
    //     {
    //         id: 4,
    //         text: 'root2',
    //         "state": {
    //             "opened": true,
    //             "disabled": true,
    //             "selected": false
    //         },
    //         children: [
    //             {
    //                 id: 5,
    //                 text: 'child2.1',
    //                 "state": {
    //                     "opened": false,
    //                     "disabled": false,
    //                     "selected": false
    //                 },
    //             },
    //             {
    //                 id: 6,
    //                 text: 'child2.2',
    //                 "state": {
    //                     "opened": false,
    //                     "disabled": false,
    //                     "selected": false
    //                 },
    //                 children: [
    //                     {
    //                         id: 7,
    //                         text: 'subsub',
    //                         "state": {
    //                             "opened": false,
    //                             "disabled": false,
    //                             "selected": false
    //                         },
    //                     }
    //                 ]
    //             }
    //         ]
    //     },
    //     {
    //         id: 8,
    //         text: 'asyncroot',
    //         "state": {
    //             "opened": false,
    //             "disabled": false,
    //             "selected": false
    //         },
    //     }
    // ];
    /***********.HIERARCHY_WIDGET*************/



    // status: Object = {
    //     navigation_panel: {
    //         collapsed: false
    //     }
    // };
}
