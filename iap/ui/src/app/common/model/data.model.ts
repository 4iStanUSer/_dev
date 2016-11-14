import {
    TimelabelInput,
    TimeLabelsModel,
    TimeLabelModel
} from "./time-labels.model";
import {
    GrowthRateInput,
    GrowthRateModel,
    GrowthRatesModel
} from "./growth.model";
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
import {TimeScalesModel, TimeScaleInput} from "./time-scales.model";



export class DataModel {
    timeScales: TimeScalesModel = null;
    timeLables: TimeLabelsModel = null;
    grRates: GrowthRatesModel = null;
    variables: VariablesModel = null;
    pointsValues: PointsValuesModel = null;

    constructor(timeScales: Array<TimeScaleInput>,
                timeLabels: Array<TimelabelInput>,
                variables: {[variable: string]: VariableInput},
                rates: {[variable: string]: Array<GrowthRateInput>},
                pointsValues: {
                    [timescale: string]: {
                        [variable: string]: Array<PointValueInput>
                    }
                }) {

        this.timeScales = new TimeScalesModel(timeScales);
        this.timeLables = new TimeLabelsModel(timeLabels);
        this.variables = new VariablesModel(variables);
        this.grRates = new GrowthRatesModel(rates);
        this.pointsValues = new PointsValuesModel(pointsValues,
            this.variables, this.timeLables);
    }


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

    getVariablesByType(type: string): Array<VariableModel> {
        let variables = Object.keys(this.variables.storage);
        let output = [];
        let l = variables.length;
        for (let i = 0; i < l; i++) {
            if (type == this.variables.storage[variables[i]].type) {
                output.push(this.variables.storage[variables[i]]);
            }
        }
        return output;
    }


    // ??????????????? TODO Review
    getCargsForPointsValues(variable: VariableModel,
                            periods: Array<{
                                'start': string,
                                'end': string
                            }>): Array<GrowthRateModel> {

        return periods.map((p) => {
            for (let i = 0; i < this.grRates.storage[variable.name].length; i++) {
                let carg = this.grRates.storage[variable.name][i];
                if (carg['start'] == p['start'] && carg['end'] == p['end']) {
                    return carg;
                }
            }
            return null;
        }, this).filter((c) => {
            return !!(c);
        });
    }



    getCagrValue(varKey: string, start: string,
                 end: string, timescale: string) {
        // TODO Implement timescale for CAGR
        try {
            for (let i = 0; i<this.grRates[varKey].length;i++) {
                if (
                    this.grRates[varKey][i].start == start
                    && this.grRates[varKey][i].end == end
                    && true // this.cargs[varKey][i].timescale == timescale
                ) {
                    return this.grRates[varKey][i].value;
                }
            }
        } catch (e) {
            // TODO Implement query for server
            return null;
        }
    }

    getFullPeriodTime

}
