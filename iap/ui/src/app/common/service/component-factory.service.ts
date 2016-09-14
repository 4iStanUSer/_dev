import {
    Injectable,
    ViewContainerRef,
    ComponentFactoryResolver
} from '@angular/core';
import * as _ from 'lodash';
import {HierarchyWidgetComponent} from './../cmp/hierarchy-widget/';
import {DropdownComponent} from './../cmp/dropdown/';
import {TimeseriesWidgetComponent} from './../cmp/timeseries-widget/';


// TODO Move this
interface IUIConfiguration {
    widgets: Object,
    not_widgets: Object
}

interface IWidgetsConfiguration {

}


@Injectable()
export class ComponentFactoryService {

    private _config: Object = null;

    private _types: { [s: string]: any; } = {
        'hierarchy': HierarchyWidgetComponent,
        'dropdown': DropdownComponent,
        'timeseries': TimeseriesWidgetComponent
    };

    constructor(private resolver: ComponentFactoryResolver) {
    }

    public setConfig(config: IWidgetsConfiguration) {
        this._config = config
    }

    public getConfig(widget_type: string, widget_name?: string) {
        if (this._config && widget_type in this._config) {
            let default_conf = ('default' in this._config[widget_type])
                ? this._config[widget_type]['default'] : {};
            let widget_conf = (
                widget_name && widget_name.length &&
                widget_name in this._config[widget_type])
                ? this._config[widget_type][widget_name] : {};
            return _.merge(default_conf, widget_conf);
        }
        return false;
    }

    public generate(cmp_type: string, container: ViewContainerRef, context: any) { //: Observable<Component>
        const widgetCmp = this.resolver.resolveComponentFactory(this._types[cmp_type]);
        let componentRef = container.createComponent(widgetCmp);
        return componentRef.instance;
    }


}


// @Injectable()
// export class ComponentFactoryService {
//     private types: { [s: string]: any; } = {
//         'hierarchy': HierarchyWidgetComponent,
//         'dropdown': DropdownComponent,
//         'timeseries': TimeseriesWidgetComponent
//     };
//
//     constructor(private resolver: ComponentResolver) { }
//
//     public generate(cmp_type: string, container: ViewContainerRef, context: any){ //: Observable<Component>
//         //if (!this.types[cmp_type]) return false;
//         return this.resolver.resolveComponent(this.types[cmp_type])
//                 .then((factory) => {
//                     let cmp = container.createComponent(factory);
//                     return cmp.instance;
//                     //observable.publish(); //cmp.instance
//                     // component.items = d;
//                     // console.info(component);
//                     //
//                     // component.itemSelected.subscribe(function(event){
//                     //     context.hierarchyItemSelect(event);
//                     // });
//                 });
//         // // let obs = Observable.();
//         // var observable = new Observable<Component>();
//         // observable.subscribe((cmp) => {
//         //     console.log(11);
//         //     console.log(cmp);
//         // });
//         // if (this.types[cmp_type]) {
//         //
//         // } else {
//         //     this.resolver.resolveComponent(this.types[cmp_type])
//         //         .then((factory) => {
//         //             let cmp = container.createComponent(factory);
//         //             //observable.publish(); //cmp.instance
//         //             // component.items = d;
//         //             // console.info(component);
//         //             //
//         //             // component.itemSelected.subscribe(function(event){
//         //             //     context.hierarchyItemSelect(event);
//         //             // });
//         //         });
//         // }
//         //
//         // return observable;
//     }
// }
