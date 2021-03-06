import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'keys'
})
/**
 * Pipe for getting list of keys of object
 */
export class KeysPipe implements PipeTransform {

    transform(value, args?: string[]): Array<string|number> {
        let keys = [];
        if ((typeof value === "object") && (value !== null)) {
            keys = Object.keys(value);
        } else {

        }
        return keys;
    }
}
