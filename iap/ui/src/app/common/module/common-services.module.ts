import {NgModule} from '@angular/core';
import {HttpModule, JsonpModule} from '@angular/http';

/*-Services-*/
import {AjaxService} from '../service/ajax.service';
import {LoadingService} from '../service/loading.service';
import {StaticDataService} from "../service/static-data.service";
import {ComponentFactoryService} from '../service/component-factory.service';
import {AuthService} from "../service/auth.service";
/*-.Services-*/

/*-Pipes-*/
import {FilterListPipe} from "../pipe/filter-list.pipe";
import {KeysPipe} from "../pipe/keys.pipe";
import {IterateObjectByOrderPipe} from "../pipe/iterate-object-by-order.pipe";
/*-.Pipes-*/

@NgModule({
    imports: [
        HttpModule,
        JsonpModule
    ],
    declarations: [
        FilterListPipe,
        KeysPipe,
        IterateObjectByOrderPipe
    ],
    providers: [
        AjaxService,
        LoadingService,
        ComponentFactoryService,
        StaticDataService,

        AuthService // TODO Review - maybe move into login module
    ],
    exports: [
        FilterListPipe,
        KeysPipe,
        IterateObjectByOrderPipe
    ]
})
/**
 * Module for all common services.
 * Main aim - make one instance of each service for all ngModules.
 */
export class CommonServicesModule {
}
