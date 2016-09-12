import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HierarchyWidgetComponent } from './hierarchy-widget.component';
import { TreeComponent, TreeNodeComponent } from './tree/';
import { SearchComponent } from './search/';

@NgModule({
    imports:[
        CommonModule,
        FormsModule
    ],
    declarations: [
        TreeNodeComponent,
        TreeComponent,
        SearchComponent,
        HierarchyWidgetComponent
    ],
    exports: [
        HierarchyWidgetComponent
    ]
})
export class HierarchyWidgetModule { }
