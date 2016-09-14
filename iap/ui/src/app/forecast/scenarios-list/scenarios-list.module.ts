import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ScenariosListComponent} from './scenarios-list.component';

@NgModule({
    imports: [
        CommonModule
    ],
    declarations: [
        ScenariosListComponent
    ],
    exports: [
        ScenariosListComponent
    ],
    providers: [ ]
})
export class ScenariosListModule { }
