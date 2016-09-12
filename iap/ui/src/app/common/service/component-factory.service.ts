import {
    Injectable,
    ViewContainerRef,
    ComponentFactoryResolver
} from '@angular/core';
import {HierarchyWidgetComponent} from './../cmp/hierarchy-widget/';
import {DropdownComponent} from './../cmp/dropdown/';
import {TimeseriesWidgetComponent} from './../cmp/timeseries-widget/';

@Injectable()
export class ComponentFactoryService {
    private types: { [s: string]: any; } = {
        'hierarchy': HierarchyWidgetComponent,
        'dropdown': DropdownComponent,
        'timeseries': TimeseriesWidgetComponent
    };

    constructor(private resolver: ComponentFactoryResolver) { }

    public generate(cmp_type: string, container: ViewContainerRef, context: any) { //: Observable<Component>
        const widgetCmp = this.resolver.resolveComponentFactory(this.types[cmp_type]);
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
