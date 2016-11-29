
export class Helper {

    /**
     * Returns property which value equals to variable 'value'
     * @param obj
     * @param value
     * @returns {string}
     */
    static findKey(obj: Object, value: any): string {
        for (var prop in obj) {
            if (obj.hasOwnProperty(prop)) {
                if (obj[prop] === value)
                    return prop;
            }
        }
    }

    /**
     * Returns range of numbers.
     * If passed only start - returns range from 0 to start value
     * If also passed stop - returns range from 'start' to 'end' with step == 1
     * If passed step too - returns range from 'start' to 'end'
     * with specified 'step'
     * @param start
     * @param stop
     * @param step
     * @returns {Array}
     */
    static range(start: number, stop?: number, step?: number) {
        if (typeof stop == 'undefined') {
            stop = start;
            start = 0;
        }
        if (typeof step == 'undefined') {
            step = 1;
        }
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }
        var result = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.push(i);
        }
        return result;
    };
}
