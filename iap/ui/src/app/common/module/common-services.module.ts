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
/*-.Pipes-*/

@NgModule({
    imports: [
        HttpModule,
        JsonpModule
    ],
    declarations: [
        FilterListPipe,
        KeysPipe
    ],
    providers: [
        AjaxService,
        LoadingService,
        ComponentFactoryService,
        StaticDataService,
        AuthService
    ],
    exports: [
        FilterListPipe,
        KeysPipe
    ]
})
export class CommonServicesModule {
}
