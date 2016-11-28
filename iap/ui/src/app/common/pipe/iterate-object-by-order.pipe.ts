import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'iterateObjectByOrder',
    pure: false
})
export class IterateObjectByOrderPipe implements PipeTransform {

    transform(orderList: Array<string>, sourceObj: Object): Array<Object> {
        return orderList.map(
            (objProp: string) => {
                return sourceObj[objProp];
            }
        );
    }
}
