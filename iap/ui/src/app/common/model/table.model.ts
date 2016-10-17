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
    parent_index: string|number;
    children?: Array<string|number>;
}
interface TimePointValueInput {
    timelabels_index: number;
    value: number|string;
    gr: number|string;
    color?: string;
    isEditable?: boolean;
    format?: string;
}


export class TableModel {
    private vars: Object = {}; // Array<Object> = [];
    private timelabels: Array<Object> = [];
    private timelabelsChildren: Array<number> = [];
    private values;

    constructor(vars: {[variableName: string]: VariableInput},
                timelabels: Array<TimeLabelInput>,
                values: {
                    [timescale: string]: {
                        [variableName: string]: Array<TimePointValueInput>
                    }
                })
    {
        let varsNamesList = Object.keys(vars);
        this.timelabels = timelabels;

        let timelabel;
        let children;
        for (let i = 0; i < this.timelabels.length; i++) {
            timelabel = this.timelabels[i];
            children = [];
            if (timelabel['parent_index'] !== null) {

            }
            this.timelabelsChildren.push(children);
        }
    }
}
