let Timelabels = [
    {
        name: 2010,
        timescale: 'annual',
        parent_index: null
    },
    {
        name: 2011,
        timescale: 'annual',
        parent_index: null
    },
    {
        name: 2012,
        timescale: 'annual',
        parent_index: null
    },
    {
        name: 2013,
        timescale: 'annual',
        parent_index: null
    },

    //

    {
        name: 'Q1',
        timescale: 'quarterly',
        parent_index: 0
    },
    {
        name: 'Q2',
        timescale: 'quarterly',
        parent_index: 0
    },
    {
        name: 'Q3',
        timescale: 'quarterly',
        parent_index: 0
    },
    {
        name: 'Q4',
        timescale: 'quarterly',
        parent_index: 0
    },

    {
        name: 'Q1',
        timescale: 'quarterly',
        parent_index: 1
    },
    {
        name: 'Q2',
        timescale: 'quarterly',
        parent_index: 1
    },
    {
        name: 'Q3',
        timescale: 'quarterly',
        parent_index: 1
    },
    {
        name: 'Q4',
        timescale: 'quarterly',
        parent_index: 1
    },

    {
        name: 'Q1',
        timescale: 'quarterly',
        parent_index: 2
    },
    {
        name: 'Q2',
        timescale: 'quarterly',
        parent_index: 2
    },
    {
        name: 'Q3',
        timescale: 'quarterly',
        parent_index: 2
    },
    {
        name: 'Q4',
        timescale: 'quarterly',
        parent_index: 2
    },
    {
        name: 'Q1',
        timescale: 'quarterly',
        parent_index: 3
    },
    {
        name: 'Q2',
        timescale: 'quarterly',
        parent_index: 3
    },
    {
        name: 'Q3',
        timescale: 'quarterly',
        parent_index: 3
    },
    {
        name: 'Q4',
        timescale: 'quarterly',
        parent_index: 3
    },

    //

    {
        name: 'Jan',
        timescale: 'monthly',
        parent_index: 4
    },
    {
        name: 'Feb',
        timescale: 'monthly',
        parent_index: 4
    },
    {
        name: 'Mar',
        timescale: 'monthly',
        parent_index: 4
    },

    {
        name: 'Jan',
        timescale: 'monthly',
        parent_index: 8
    },
    {
        name: 'Feb',
        timescale: 'monthly',
        parent_index: 8
    },
    {
        name: 'Mar',
        timescale: 'monthly',
        parent_index: 8
    },
];

let Variables = {
    CPI: {
        name: 'CPI',
        metric: 'index',
        multiplier: null,
        type: 'driver', // | 'output',
        driver_type: 'economic' // | null
    },
    GDP: {
        name: 'GDP',
        metric: 'index',
        multiplier: null,
        type: 'driver',
        driver_type: 'economic'
    },
    sales: {
        name: 'Sales',
        metric: '$',
        multiplier: 'MM',
        type: 'output',
    },
    volume: {
        name: 'Volume',
        metric: 'EQ',
        multiplier: 'Thousands',
        type: 'output'
    },
    price: {
        name: 'Price',
        metric: 'per EQ',
        multiplier: '$',
        type: 'output'
    }
};

let Data = {
    annual: {
        sales: [
            {
                'timelabels_index': 0,
                'value': 0,
                'gr': 15,
                // 'color',
                // 'isEditable',
                // 'format'
            },
            {
                'timelabels_index': 1,
                'value': 1,
                'gr': 15
            },
            {
                'timelabels_index': 2,
                'value': 2,
                'gr': 15
            },
            {
                'timelabels_index': 3,
                'value': 3,
                'gr': 15
            }
        ],
        volume: [
            {
                'timelabels_index': 0,
                'value': 4,
                'gr': 15
            },
            {
                'timelabels_index': 1,
                'value': 5,
                'gr': 15
            },
            {
                'timelabels_index': 2,
                'value': 6,
                'gr': 15
            },
            {
                'timelabels_index': 3,
                'value': 7,
                'gr': 15
            }
        ],
        price: [
            {
                'timelabels_index': 0,
                'value': 4,
                'gr': 15
            },
            {
                'timelabels_index': 1,
                'value': 5,
                'gr': 15
            },
            {
                'timelabels_index': 2,
                'value': 6,
                'gr': 15
            },
            {
                'timelabels_index': 3,
                'value': 7,
                'gr': 15
            }
        ]
    },
    quarterly: {
        sales: [
            {
                'timelabels_index': 4,
                'value': 8,
                'gr': 15
            },
            {
                'timelabels_index': 5,
                'value': 9,
                'gr': 15
            },
            {
                'timelabels_index': 6,
                'value': 10,
                'gr': 15
            },
            {
                'timelabels_index': 7,
                'value': 11,
                'gr': 15
            },
        ],
        volume: [
            {
                'timelabels_index': 4,
                'value': 12,
                'gr': 15
            },
            {
                'timelabels_index': 5,
                'value': 13,
                'gr': 15
            },
            {
                'timelabels_index': 6,
                'value': 14,
                'gr': 15
            },
            {
                'timelabels_index': 7,
                'value': 15,
                'gr': 15
            },
        ],
        price: [
            {
                'timelabels_index': 4,
                'value': 12,
                'gr': 15
            },
            {
                'timelabels_index': 5,
                'value': 13,
                'gr': 15
            },
            {
                'timelabels_index': 6,
                'value': 14,
                'gr': 15
            },
            {
                'timelabels_index': 7,
                'value': 15,
                'gr': 15
            },
        ]
    },
    monthly: {
        sales: [
            {
                'timelabels_index': 20,
                'value': 16,
                'gr': 15
            },
            {
                'timelabels_index': 21,
                'value': 17,
                'gr': 15
            },
            {
                'timelabels_index': 22,
                'value': 18,
                'gr': 15
            },
            {
                'timelabels_index': 23,
                'value': 19,
                'gr': 15
            },
            {
                'timelabels_index': 24,
                'value': 20,
                'gr': 15
            },
            {
                'timelabels_index': 25,
                'value': 21,
                'gr': 15
            }
        ],
        volume: [
            {
                'timelabels_index': 20,
                'value': 22,
                'gr': 15
            },
            {
                'timelabels_index': 21,
                'value': 23,
                'gr': 15
            },
            {
                'timelabels_index': 22,
                'value': 24,
                'gr': 15
            },
            {
                'timelabels_index': 23,
                'value': 25,
                'gr': 15
            },
            {
                'timelabels_index': 24,
                'value': 26,
                'gr': 15
            },
            {
                'timelabels_index': 25,
                'value': 27,
                'gr': 15
            }
        ],
        price: [
            {
                'timelabels_index': 20,
                'value': 22,
                'gr': 15
            },
            {
                'timelabels_index': 21,
                'value': 23,
                'gr': 15
            },
            {
                'timelabels_index': 22,
                'value': 24,
                'gr': 15
            },
            {
                'timelabels_index': 23,
                'value': 25,
                'gr': 15
            },
            {
                'timelabels_index': 24,
                'value': 26,
                'gr': 15
            },
            {
                'timelabels_index': 25,
                'value': 27,
                'gr': 15
            }
        ]
    }
};


interface VariableInput {
    name: string;
    metric: string;
    multiplier: string;
    type: string; // 'driver' | 'output'
    driver_type: string|null; // 'economic' | ... | null
}
interface TimeLabelInput {
    name: string|number;
    timescale: string;
    parent_index: number;
    children?: Array<string|number>;
}
interface TimePointValueInput {
    timestamp: string;
    value: number|string;
    gr: number|string;
    color?: string;
    isEditable?: boolean;
    format?: string;
}


/***********************CLASSES**********************/
class CellModel {
    // options: CellOptions = {};

    constructor(public variable: string,
                public timelabel: string,
                public value: number|string) {
    }
}

class TimePointModel {
    id: number = null;
    children: Array<TimePointModel> = [];
    parent: TimePointModel = null;
    depth: number = 0;

    ////////////////////////

    timelabels: {[timelabel: string]: string}
    variables: {[variable: string]: CellModel} = {};

    data: Object = {};



    // options: RowOptions = {};


    isShown: boolean = true;
    isExpanded: boolean = false;

    isHeader: boolean = false;

    // constructor(id: number, tblRow: TblRow, parent: RowModel, is_header: boolean = false) {
    //     this.id = id;
    //     this.isHeader = is_header;
    //     this.meta = [tblRow['meta']];
    //     this.data = tblRow['data'];
    //     if (parent !== null) {
    //         this.depth = parent.depth + 1;
    //         this.isShown = false;
    //         this.parent = parent;
    //         parent.children.push(this);
    //     }
    // }
}

export class TableModel {
    private config: Object = {
        'isEditable': true,
        'rowsMode': 'time', // 'variables'
    };

    private flatCellsStorage: Array<CellModel> = [];
    private flatTimePointsStorage: Array<TimePointModel> = [];

    private scalesOrder: Array<string> = [];

    private vars: Object = {}; // Array<Object> = [];
    // private timelabels: Array<Object> = [];
    // private timelabelsChildren: Array<number> = [];
    private values;

    constructor(vars: {[variableName: string]: VariableInput},
                timelabels: Array<TimeLabelInput>,
                data: {
                    [timescale: string]: {
                        [variableName: string]: Array<TimePointValueInput>
                    }
                }) {
        let varsNamesList = Object.keys(vars);
        // this.timelabels = timelabels;

        this.processInput(timelabels, data);

    }


    private processInput(timelabels: Array<TimeLabelInput>,
                         data: Object): void {
        this.scalesOrder = [];

        timelabels = Timelabels; // TODO Remove this: testing code <-

        let pIndex: number = null;
        let ts: string = null;
        let relations: { [s: string]: string; } = {}; // {child: parent}

        for (let i = 0; i < timelabels.length; i++) {
            pIndex = timelabels[i]['parent_index'];
            ts = timelabels[i]['timescale'];

            if (!('children' in timelabels[i])) {
                timelabels[i]['children'] = [];
            }

            if (pIndex !== null) {
                if (!timelabels[pIndex]) {
                    console.error('Not found such index ' + pIndex);
                    break;
                }
                if (!('children' in timelabels[pIndex])) {
                    timelabels[pIndex]['children'] = [];
                }
                timelabels[pIndex]['children'].push(i);
            }
            if (!(ts in relations)) {
                if (pIndex !== null) {
                    relations[ts] = timelabels[pIndex]['timescale'];
                } else {
                    relations[ts] = null;
                }
            }
        }

        let parentTS = Helper.findKey(relations, null);
        if (parentTS) {
            this.scalesOrder.push(parentTS);
            let relLength = Object.keys(relations).length;
            let childTS = null;
            while (relLength != this.scalesOrder.length) {
                childTS = Helper.findKey(relations, parentTS);
                if (childTS) {
                    this.scalesOrder.push(childTS);
                    parentTS = childTS;
                } else {
                    console.error('Something wrong: have no such value');
                    break;
                }
            }
        }

        let addedTimelabels = {};
        this.addTimePoints(timelabels, Helper.range(timelabels.length-1),
            addedTimelabels);

    }

    private addTimePoints(entireList: Array<Object>,
                    indexesToProcess: Array<number>,
                    addedIndexes: Object,
                    parent: TimePointModel = null): void {

        for (let i = 0; i < indexesToProcess.length; i++) {
            if (!addedIndexes[indexesToProcess[i]]) {
                addedIndexes[indexesToProcess[i]] = true;

                // Add row into this.flatRowsStorage
                let timePoint = new TimePointModel();
                timePoint.id = indexesToProcess[i];
                if (parent !== null) {
                    timePoint.parent = parent;
                    timePoint.depth = parent.depth + 1;
                    parent.children.push(timePoint);
                }
                this.flatTimePointsStorage.push(timePoint);

                // Add row's children into this.flatRowsStorage
                if (entireList[indexesToProcess[i]]['children'].length > 0) {
                    this.addTimePoints(entireList,
                        entireList[indexesToProcess[i]]['children'],
                        addedIndexes,
                        timePoint);
                }
            }
        }
    }


}

class Helper {

    static findKey(obj: Object, value: any): string {
        for (var prop in obj) {
            if (obj.hasOwnProperty(prop)) {
                if (obj[prop] === value)
                    return prop;
            }
        }
    }

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
