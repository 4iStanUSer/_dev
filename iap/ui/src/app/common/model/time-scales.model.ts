export interface TimeScaleInput {
    key: string;
    name: string;
    growth_lag: number;
}

export class TimeScalesModel {
    order: Array<string> = [];
    storage: {
        [timescale: string]: {
            key: string;
            name: string;
            growth_lag: number;
        }
    } = null;

    constructor(input: Array<TimeScaleInput>) {
        if (input && input.length) {
            let l = input.length;
            this.storage = {};
            for (let i = 0; i < l; i++) {
                this.order.push(input[i].key);
                this.storage[input[i].key] = input[i];
            }
        }
    }

    getTimeScale(timescale: string) {
        return (this.storage[timescale]) ? this.storage[timescale] : null;
    }
}
