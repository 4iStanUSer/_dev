
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
interface ValuesInput {
    [timescale: string]: {
        [variableName: string]: Array<TimePointValueInput>
    }
}

/***********************CLASSES**********************/

export class DataCell {
    value: any = null;
    editMode: boolean = false;
    isEditable: boolean = true; // TODO Revert false (VL)
    isChanged: boolean = false;

    variable: string = null;
    timescale: string = null;
    timelabel: string = null;

    constructor(public id: number,
                public data: Object) {
        if (data['isEditable']) {
            this.isEditable = true;
        }
    }

    getValue() {
        return this.data['value'];
    }


    setEditMode() {
        if (this.isEditable) {
            this.value = this.data['value'];
            this.editMode = true;
            return true;
        }
        return false;
    }

    isValid(value) {
        return true;
        //return Number.isInteger(value);
    }

    save() {
        if (this.isEditable && this.isValid(this.value)) {
            this.data['value'] = this.value;
            this.editMode = false;
            this.value = null;
            this.isChanged = true;
            return true;
        }
        return false;
    }
    cancel() {
        this.editMode = false;
        this.value = null;
    }

    getChange() {
        return {
            'variable': this.variable,
            'timescale': this.timescale,
            'timelabel': this.timelabel,
            'value': this.data['value']
        };
    }
}

export class RowModel {
    id: number|string = null;
    meta: Array<Object> = [];
    cells: Array<DataCell> = [];
    children: Array<RowModel> = [];
    parent: RowModel = null;
    depth: number = 0;
    isShown: boolean = true;
    isExpanded: boolean = false;

    // isHeader: boolean = false;
    // options: RowOptions = {};

    constructor(id: number,
                tblRow: {meta: Array<Object>, cells: Array<DataCell>},
                parent: RowModel = null
                ) { // is_header: boolean = false
        this.id = id;
        // this.isHeader = is_header;
        this.meta = tblRow['meta'];
        this.cells = tblRow['cells'];
        if (parent !== null) {
            this.depth = parent.depth + 1;
            this.isShown = false;
            this.parent = parent;
            parent.children.push(this);
        }
    }


    public changeExpandStatus() {
        if (this.children && this.children.length) {
            let expandStatus = !this.isExpanded;
            this.isExpanded = expandStatus;

            this.children.forEach((child: RowModel) => {
                if (false === expandStatus) {
                    child.hideBranch();
                } else {
                    child.showBranch();
                }
            });
        }
    }

    public showBranch() {
        this.isShown = true;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                if (this.isExpanded) {
                    child.showBranch();
                }
            });
        }
    }

    public hideBranch() {
        this.isShown = false;
        if (this.children && this.children.length) {
            this.children.forEach((child: RowModel) => {
                child.hideBranch();
            });
        }
    }

}

export class TableModel {
    private config: Object = { // TODO Implement configuration (VL)
        'isEditable': true,
        'asRows': null, // 'time_points' || 'variables'
        'valueField': 'value', // || 'growth'
    };
    public dataCellStorage = [];
    private dataRowStorage = [];

    vars: {[variableName: string]: VariableInput} = {};
    timelabels: Array<TimeLabelInput> = [];
    data: ValuesInput = {};

    mode: string = null;
    timeHierarchy = [];
    timelabelsOrder = [];
    scalesOrder: Array<string> = [];
    dataMap: {
        [timescale: string]: {
            [variableName: string]: {
                [timestamp: string]: number
            }
        }
    } = {};

    columnsOrder: Array<string> = [];

    constructor(mode: string,
                vars: {[variableName: string]: VariableInput},
                timelabels: Array<TimeLabelInput>,
                data: ValuesInput) {
        if (mode && ['time_points', 'variables'].indexOf(mode) != -1) {
            this.mode = mode;
            this.vars = vars;
            this.timelabels = timelabels; //timelabels;
            this.data = data;

            this.makeTimeHierarchy(this.timelabels);
            this.makeTimelabelsOrder(this.timelabels,
                Helper.range(this.timelabels.length - 1), {});
            this.makeDataMapping(this.data, this.timelabels);
            if ('time_points' == this.mode) {
                this.columnsOrder = Object.keys(this.vars);
            } else if ('variables' == this.mode) {
                // TODO Implement
            }
        } else {
            console.error('Wrong mode for TableModel');
        }
    }

    getHeader() {
        if ('time_points' == this.mode) {
            let rows = [
                {
                    meta: [{
                        text: 'Driver'
                    }],
                    cells: this.columnsOrder.map((variable) => {
                        return {
                            text: this.vars[variable]['name']
                        }
                    })
                },
                {
                    meta: [{
                        text: 'Metric'
                    }],
                    cells: this.columnsOrder.map((variable) => {
                        return {
                            'text': this.vars[variable]['metric']
                        }
                    })
                }
            ];
            return rows;
        } else if ('variables' == this.mode) {
            // TODO Implement
        }
    }

    getBody() {
        if ('time_points' == this.mode) {
            this.getRowsModels(this.timelabels, this.timelabelsOrder, {});
            return this.dataRowStorage;
        } else if ('variables' == this.mode) {
            // TODO Implement
        }
    }



    private getRowsModels(source: Array<Object>,
                          listToAdd: Array<number>,
                          addedIndexes: Object,
                          parent: RowModel = null) { // TODO Remake (VL)
        let models = [];
        for (let i = 0; i < listToAdd.length; i++) {
            if (source[listToAdd[i]] && !addedIndexes[listToAdd[i]]) {
                addedIndexes[listToAdd[i]] = true;
                let timelabel = source[listToAdd[i]];
                let timescale = timelabel['timescale'];
                let timestamp = timelabel['full_name'];

                let model = new RowModel(this.dataRowStorage.length, {
                    meta: [{
                        text: timelabel['full_name']
                    }],
                    cells: this.columnsOrder.map((variable) => {
                        let idx = this.dataMap[timescale][variable][timestamp];
                        let cell = new DataCell(this.dataCellStorage.length,
                            this.data[timescale][variable][idx]);

                        cell.variable = variable;
                        cell.timescale = timescale;
                        cell.timelabel = timestamp;

                        this.dataCellStorage.push(cell);
                        return cell;
                    }, this)
                }, parent);
                this.dataRowStorage.push(model);
                if (this.timeHierarchy[listToAdd[i]].length) {
                    this.getRowsModels(source, this.timeHierarchy[listToAdd[i]], addedIndexes, model);
                }
            }
        }
        return models;
    }


    private makeDataMapping(data: Object,
                            timelabels: Array<TimeLabelInput>): void {
        this.dataMap = {};
        for (let scale in data) {
            this.dataMap[scale] = {};
            for (let variable in data[scale]) {
                this.dataMap[scale][variable] = {};
                for (let i = 0; i < data[scale][variable].length; i++) {
                    let timestamp = data[scale][variable][i]['timestamp'];
                    let found = timelabels.findIndex((el) => {
                        return (el['timescale'] == scale
                        && el['full_name'] == timestamp) ? true : false;
                    });
                    this.dataMap[scale][variable][timestamp] = (found != -1)
                        ? found : null;
                }
            }
        }
    }

    private makeTimeHierarchy(timelabels: Array<TimeLabelInput>): void {
        this.scalesOrder = [];
        this.timeHierarchy = [];

        let pIndex: number = null;
        let ts: string = null;
        let relations: { [s: string]: string; } = {}; // {child: parent}

        this.timeHierarchy = timelabels.map(() => {
            return []
        });

        for (let i = 0; i < timelabels.length; i++) {
            pIndex = timelabels[i]['parent_index'];
            ts = timelabels[i]['timescale'];
            if (pIndex !== null) {
                try {
                    this.timeHierarchy[pIndex].push(i);
                } catch (e) {
                    console.error('Not found such index ' + pIndex);
                }
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
    }

    private makeTimelabelsOrder(fullList: Array<TimeLabelInput>,
                                listToAdd: Array<number>,
                                alreadyAdded: Object): void {
        for (let i = 0; i < listToAdd.length; i++) {
            if (!alreadyAdded[listToAdd[i]] && fullList[listToAdd[i]]) {

                alreadyAdded[listToAdd[i]] = true;

                this.timelabelsOrder.push(listToAdd[i]);

                // Add children into this.flatRowsStorage
                if (this.timeHierarchy[listToAdd[i]].length > 0) {
                    this.makeTimelabelsOrder(fullList,
                        this.timeHierarchy[listToAdd[i]],
                        alreadyAdded);
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
