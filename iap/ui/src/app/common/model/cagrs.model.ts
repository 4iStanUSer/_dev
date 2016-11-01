export interface CagrInput {
    start: string;
    end: string;
    value: number;
}

export class CagrModel {
    constructor(public start: string, public end: string,
                public value: number) { }
}

export class CagrsModel { // TODO Refactor storage structure (VL)
    public storage: {
        [variable: string]: Array<CagrModel>
    };

    // TODO connect with timelabels (VL)

    constructor(input: {[variable: string]: Array<CagrInput>}) {
        this.storage = {};
        for (let variable in input) {
            this.storage[variable] = [];
            for (let i = 0; i<input[variable].length; i++) {
                let cagr = new CagrModel(input[variable]['start'],
                    input[variable]['end'],
                    input[variable]['value']);
                this.storage[variable].push(cagr);
            }
        }
    }
}
