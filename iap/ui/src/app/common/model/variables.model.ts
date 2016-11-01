export interface VariableInput {
    metric: string;
    multiplier: number;
    name: string;
    type: string;
}

export class VariableModel {
    constructor(
        public name: string,
        public metric: string,
        public multiplier: number,
        public type: string
    ) { }
}

export class VariablesModel { // TODO Refactor storage structure (VL)

    public storage: {[variable: string]: VariableModel} = null;

    constructor(input: {[variable: string]: VariableInput}) {
        this.storage = {};
        for (let variable in input) {
            let v = new VariableModel(
                input[variable]['name'],
                input[variable]['metric'],
                input[variable]['multiplier'],
                input[variable]['type']
            );
            this.storage[variable] = v;
        }
    }

    get(varName: string){
        return (varName in this.storage) ? this.storage[varName] : null;
    }
}
