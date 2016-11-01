import {VariablesModel, VariableModel} from "./variables.model";
import {TimeLabelsModel, TimeLabelModel} from "./time-labels.model";

export interface PointValueInput {
    value: number;
    timestamp: string;
    gr: number;
}

export class PointValueModel {
    variable: VariableModel;
    timelabel: TimeLabelModel;

    constructor(public timestamp: string, public value: number,
                public gr: number) { }
}

export class PointsValuesModel { // TODO Refactor storage structure (VL)
    public storage: {
        [timescale: string]: {
            [variable: string]: Array<PointValueModel>
        }
    };

    // TODO connect with timelabels (VL)

    constructor(
        input: {
            [timescale: string]: {
                [variable: string]: Array<PointValueInput>
            }
        },
        variables: VariablesModel,
        timeLabels: TimeLabelsModel
    ) {
        this.storage = {};

        for (let timescale in input) {
            this.storage[timescale] = {};

            // TODO Should make TimescaleModel

            for (let variable in input[timescale]) {
                this.storage[timescale][variable] = [];
                let v = variables.get(variable);
                for (let i = 0; i<input[timescale][variable].length; i++) {
                    let pointV = new PointValueModel(
                        input[timescale][variable][i]['timestamp'],
                        input[timescale][variable][i]['value'],
                        input[timescale][variable][i]['gr']
                    );

                    if (v) {
                        pointV.variable = v;
                    }
                    let t = timeLabels.getTimeLabel(
                        timescale,
                        input[timescale][variable][i]['timestamp']
                    );
                    if (t) {
                        pointV.timelabel = t;
                    }

                    this.storage[timescale][variable].push(pointV);
                }
            }
        }
    }
}
