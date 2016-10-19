import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'filterList',
    pure: false
})
export class FilterListPipe implements PipeTransform {

    transform(list: Array<any>, args: {key: string, value: any}): Array<any> {
        return list.filter(item => {
            return !!(args['key'] in item && item[args['key']] === args['value']);
        });
    }

}
