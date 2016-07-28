import { Component } from '@angular/core';
import { TimeseriesWidgetComponent } from './../../common/cmp/timeseries-widget/';
import { HierarchyWidgetComponent } from './../../common/cmp/hierarchy-widget/';
import { DropdownComponent } from './../../common/cmp/dropdown/';
// import { NavagationPanelComponent } from './../components/navigation_panel.component';
// import { RequestService } from './../services/request.service';

@Component({
    moduleId: module.id,
    selector: 'forecast-index-page',
    directives: [
        TimeseriesWidgetComponent,
        HierarchyWidgetComponent,
        // NavagationPanelComponent,
        DropdownComponent
    ],
    providers: [],
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

        <dropdown [items]="__DROPDOWN_ITEMS" [configuration]="__DROPDOWN_CONFIG" (changeSelection)="dropdownSelectionChanged($event)"></dropdown>

        <hierarchy-widget [items]="__HIERARCHY_ITEMS" (itemSelected)="hierarchyItemSelect($event)"></hierarchy-widget>

        <hierarchy-widget [items]="__HIERARCHY_ITEMS1" (itemSelected)="hierarchyItemSelect($event)"></hierarchy-widget>

        
    </navigation-panel>

    <div class="col-sm-9" id="cont_panel">
        <h1>main content</h1>

        <timeseries-widget [timeseries]="__TIMESERIES" [options]="__TIMESERIES_OPT"></timeseries-widget>

    </div>
</div>
`
})
export class IndexPageComponent {
    status: Object = {
        navigation_panel: {
            collapsed: false
        }
    };
    //constructor(private machinegunner: MachineGunnerService) {
    //    //let newMenuItem = {
    //    //    "name": '<i class="fa fa-bars" aria-hidden="true"></i>',
    //    //    "disabled": false
    //    //};
    //    //this.machinegunner.fire('add_menu_item',
    //    //    { newItem: newMenuItem, position: 0 });
    //}

    // constructor(private request: RequestService) { }

    private get_data_: Object = {};
    ngOnInit() {
        // this.request
        //     .get({
        //         url: '/forecasting/get_data',
        //         data: {
        //             param: '123',
        //             param2: 456,
        //             param3: [7, 8, 9]
        //         }
        //     })
        //     .subscribe(
        //         (d) => {
        //             console.log(d);
        //             this.get_data_ = d;
        //         },
        //         (e) => {
        //             console.log(e);
        //         },
        //         () => {
        //             console.log('Complete!');
        //         }
        // );
    }
    /***********DROPDOWN*************/
    dropdownSelectionChanged(e: Object) {
        console.log(e);
    }
    public __DROPDOWN_CONFIG = {
        'multiple': false,
    };
    public __DROPDOWN_ITEMS: Array<Object> = [
        {
            "id": 27524, "text": "First variant",
            "state": {
                "disabled": false,
                "selected": false
            },
        },
        {
            "id": 27525, "text": "ss1",
            "state": {
                "disabled": true,
                "selected": false
            },
        },
        {
            "id": 27526, "text": "ss2",
            "state": {
                "disabled": false,
                "selected": false
            },
        },
        {
            "id": 27527, "text": "dd",
            "state": {
                "disabled": false,
                "selected": false
            },
        },
        {
            "id": 27530, "text": "Some another",
            "state": {
                "disabled": false,
                "selected": true
            },
        },
    ];
    /***********DROPDOWN*************/
    /***********TIMESERIES*************/
    public __TIMESERIES: Array<Object> = [
        {
            head: [
                {
                    value: 'Population',
                    meta: 'Variable'
                },
                {
                    value: 'Billion',
                    meta: 'Metric'
                }
            ],
            cells: [
                {
                    value: 123,
                    valueType: 'int',
                    meta: 'April'
                },
                {
                    value: 124,
                    valueType: 'int',
                    meta: 'May'
                },
                {
                    value: 125,
                    valueType: 'int',
                    meta: 'June'
                },
                {
                    value: 126,
                    valueType: 'int',
                    meta: 'July'
                }
            ],
            options: {}
        },
        {
            head: [
                {
                    value: 'GDP',
                    meta: 'Variable'
                },
                {
                    value: '$',
                    meta: 'Metric'
                }
            ],
            cells: [
                {
                    value: 1230,
                    valueType: 'int',
                    meta: 'April'
                },
                {
                    value: 1240,
                    valueType: 'int',
                    meta: 'May'
                },
                {
                    value: 1250,
                    valueType: 'int',
                    meta: 'June'
                },
                {
                    value: 1260,
                    valueType: 'int',
                    meta: 'July'
                }
            ],
            options: {}
        }
    ]
    public __TIMESERIES_OPT = {}

    /***********.TIMESERIES*************/

    /***********HIERARCHY_WIDGET*************/
    public hierarchyItemSelect(item) {
        console.info('App Component, in hierarchy widget selected item');
        console.info(item)
    }
    public __HIERARCHY_ITEMS: Array<Object> = [
        {
            "id": 27536, "text": "New node", "type": "parent",
            "state": {
                "opened": true,
                "disabled": false,
                "selected": true
            },
            "children": [
                { "id": 27524, "text": "ss", "type": "parent", "children": false },
                { "id": 27521, "text": "ss", "type": "child", "children": false }
            ]
        },
        {
            "id": 27529, "text": "New node", "type": "parent", "children": false
        },
        {
            "id": 27532, "text": "New node", "type": "child",
            "state": {
                "opened": false,
                "disabled": true,
                "selected": false
            },
            "children": false
        },
        {
            "id": 27538, "text": "New node", "type": "parent",
            "state": {
                "opened": false,
                "disabled": false,
                "selected": false
            },
            "children": [
                { "id": 7524, "text": "ss", "type": "parent", "children": false },
                { "id": 7521, "text": "ss", "type": "child", "children": false }
            ]
        }
    ];
    public __HIERARCHY_ITEMS1 = [
        {
            id: 1, text: 'root1',
            "state": {
                "opened": false,
                "disabled": false,
                "selected": false
            },
            children: [
                {
                    id: 2,
                    text: 'child1',
                    "state": {
                        "opened": false,
                        "disabled": false,
                        "selected": true
                    },
                }, {
                    id: 3,
                    text: 'child2',
                    "state": {
                        "opened": false,
                        "disabled": false,
                        "selected": false
                    },
                }
            ]
        },
        {
            id: 4,
            text: 'root2',
            "state": {
                "opened": true,
                "disabled": true,
                "selected": false
            },
            children: [
                {
                    id: 5,
                    text: 'child2.1',
                    "state": {
                        "opened": false,
                        "disabled": false,
                        "selected": false
                    },
                },
                {
                    id: 6,
                    text: 'child2.2',
                    "state": {
                        "opened": false,
                        "disabled": false,
                        "selected": false
                    },
                    children: [
                        {
                            id: 7,
                            text: 'subsub',
                            "state": {
                                "opened": false,
                                "disabled": false,
                                "selected": false
                            },
                        }
                    ]
                }
            ]
        },
        {
            id: 8,
            text: 'asyncroot',
            "state": {
                "opened": false,
                "disabled": false,
                "selected": false
            },
        }
    ];
    /***********.HIERARCHY_WIDGET*************/
}
