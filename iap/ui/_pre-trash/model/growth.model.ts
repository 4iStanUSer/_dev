export interface GrowthRateInput {
    timescale: string;
    start: string;
    end: string;
    value: number;
}

export class GrowthRateModel {
    constructor(public timescale: string, public start: string,
                public end: string, public value: number) {
    }
}

export class GrowthRatesModel { // TODO Refactor storage structure (VL)
    public storage: {
        [variable: string]: Array<GrowthRateModel>
    } = {};

    // TODO connect with timelabels (VL)

    constructor(input: {[variable: string]: Array<GrowthRateInput>}) {
        for (let variable in input) {
            this.storage[variable] = [];
            let l = input[variable].length;
            for (let i = 0; i < l; i++) {
                let growthRate = new GrowthRateModel(
                    input[variable][i]['timescale'],
                    input[variable][i]['start'],
                    input[variable][i]['end'],
                    input[variable][i]['value']
                );
                this.storage[variable].push(growthRate);
            }
        }
    }
}
