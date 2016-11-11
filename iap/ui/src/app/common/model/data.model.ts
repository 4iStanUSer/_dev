import {
    TimelabelInput,
    TimeLabelsModel,
    TimeLabelModel
} from "./time-labels.model";
import {
    CagrInput,
    CagrsModel,
    CagrModel
} from "./cagrs.model";
import {
    PointValueInput,
    PointsValuesModel,
    PointValueModel
} from "./points-values.model";
import {
    VariableInput,
    VariablesModel,
    VariableModel
} from "./variables.model";


export class DataModel {
    timeLables: TimeLabelsModel = null;
    cargs: CagrsModel = null;
    variables: VariablesModel = null;
    pointsValues: PointsValuesModel = null;

    constructor(timeLabels: Array<TimelabelInput>,
                variables: {[variable: string]: VariableInput},
                cagrs: {[variable: string]: Array<CagrInput>},
                pointsValues: {
                    [timescale: string]: {
                        [variable: string]: Array<PointValueInput>
                    }
                }) {

        this.timeLables = new TimeLabelsModel(timeLabels);
        this.variables = new VariablesModel(variables);
        this.cargs = new CagrsModel(cagrs);
        this.pointsValues = new PointsValuesModel(pointsValues,
            this.variables, this.timeLables);
    }

    // TODO Fill DataModel with methods (VL)

    getTimeLine(timescale: string, start: string,
                end: string): Array<TimeLabelModel> {
        let allTL: Array<TimeLabelModel> =
            this.timeLables.getScaleTimelabels(timescale);
        let filteredTL = [];
        let toAdd = false;
        for (let i = 0; i < allTL.length; i++) {
            if (!toAdd && allTL[i].getName() == start) {
                toAdd = true;
            }
            if (toAdd) {
                filteredTL.push(allTL[i]);
                if (allTL[i].getName() == end) {
                    break;
                }
            }
        }
        return filteredTL;
    }

    getPlainTimeLabels(): Array<TimeLabelModel> {
        return this.timeLables.storage; // TODO Make right
    }

    getVariable(name: string): VariableModel {
        return this.variables.storage[name];
    }

    getPointsValue(timescaleKey: string, variableKey: string,
                   timeline: Array<string>): Array<PointValueModel> {

        let pointsValue = [];
        for (let i = 0; i < this.pointsValues.storage[timescaleKey][variableKey].length; i++) {
            let timestamp = this.pointsValues.storage[timescaleKey][variableKey][i]['timestamp'];
            if (timeline.indexOf(timestamp) != -1) {
                pointsValue.push(this.pointsValues.storage[timescaleKey][variableKey][i]);
            }
        }
        return pointsValue;
    }


    // ??????????????? TODO Review
    getCargsForPointsValues(variable: VariableModel,
                            periods: Array<{
                                'start': string,
                                'end': string
                            }>): Array<CagrModel> {

        return periods.map((p) => {
            for (let i = 0; i < this.cargs.storage[variable.name].length; i++) {
                let carg = this.cargs.storage[variable.name][i];
                if (carg['start'] == p['start'] && carg['end'] == p['end']) {
                    return carg;
                }
            }
            return null;
        }, this).filter((c) => {
            return !!(c);
        });
    }

    getVariablesByType(type: string): Array<VariableModel> {
        let variables = Object.keys(this.variables.storage);
        let output = [];
        for (let i = 0; i < variables.length; i++) {
            if (type == this.variables.storage[variables[i]].type) {
                output.push(this.variables.storage[variables[i]]);
            }
        }
        return output;
    }

    getCagrValue(varKey: string, start: string,
                 end: string, timescale: string) {
        // TODO Implement timescale for CAGR
        try {
            for (let i = 0; i<this.cargs[varKey].length;i++) {
                if (
                    this.cargs[varKey][i].start == start
                    && this.cargs[varKey][i].end == end
                    && true // this.cargs[varKey][i].timescale == timescale
                ) {
                    return this.cargs[varKey][i].value;
                }
            }
        } catch (e) {
            // TODO Implement query for server
            return null;
        }
    }

}
