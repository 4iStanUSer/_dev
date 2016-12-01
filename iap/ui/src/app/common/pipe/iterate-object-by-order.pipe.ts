import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'iterateObjectByOrder',
    pure: false
})
/**
 * Pipe for iterating sourceObj properties with order, specified in orderList
 */
export class IterateObjectByOrderPipe implements PipeTransform {

    transform(orderList: Array<string>, sourceObj: Object): Array<Object> {
        return orderList.map(
            (objProp: string) => {
                return sourceObj[objProp];
            }
        );
    }
}
