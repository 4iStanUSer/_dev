export interface DecompositionItemInput {
    start: string;
    end: string;
    [variable: string]: any; //Array<DecompositionFactorInput>
}
interface DecompositionFactorInput {
    name: string;
    value: number;
    growth: number;
    children: any;
}

class DecompositionFactorModel {
    constructor(public name: string,
                public value: number,
                public growth: number,
                public children: any) {
    }
}

class DecompositionItemModel {
    types: {[type: string]: Array<DecompositionFactorModel>} = null;

    constructor(public start: string,
                public end: string) {
    }

    addType(type: string, factors: any) { //Array<DecompositionFactorInput>
        if (!this.types) {
            this.types = {};
        }
        this.types[type] = [];
        for (let i = 0; i < factors.length; i++) {
            let factor = factors[i];
            this.types[type].push(
                new DecompositionFactorModel(
                    factor['name'],
                    factor['value'],
                    factor['growth'],
                    factor['children']
                )
            );
        }
    }

    getTypeData(type: string) {
        return (type in this.types) ? this.types[type] : null;
    }
}

export class DecompositionModel {

    storage: Array<DecompositionItemModel> = [];

    types: Array<string> = [];

    constructor(types: Array<string>, data: Array<DecompositionItemInput>) {
        this.storage = [];

        this.types = types;
        let typesCount = this.types.length;
        if (typesCount > 0) {
            for (let i = 0; i < data.length; i++) {
                let item = new DecompositionItemModel(data[i].start,
                    data[i].end);
                for (let j = 0; j < typesCount; j++) {
                    let type = this.types[j];
                    if (data[i][type]) {
                        item.addType(type, data[i][type]);
                    }
                }
                this.storage.push(item);
            }
        }
    }

    getDecomposition(type: string, start: string, end: string) {
        let l = this.storage.length;
        for (let i = 0; i < l; i++) {
            if (this.storage[i].start == start
                && this.storage[i].end == end) {
                return this.storage[i].getTypeData(type);
            }
        }
    }

    getDecompositionTypes() {
        return this.types;
    }

    hasDecomposition(start: string, end: string): boolean {
        let l = this.storage.length;
        for (let i = 0; i < l; i++) {
            if (this.storage[i].start == start
                && this.storage[i].end == end) {
                return true;
            }
        }
        return false;
    }
}
