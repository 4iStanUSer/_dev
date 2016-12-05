import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'filterList',
    pure: false
})
/**
 * Pipe for filtering array of objects by property value of each object
 */
export class FilterListPipe implements PipeTransform {

    transform(list: Array<any>, args: {key: string, value: any}): Array<any> {
        return list.filter(item => {
            return !!(args['key'] in item && item[args['key']] === args['value']);
        });
    }

}
