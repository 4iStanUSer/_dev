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

    /**
     *
     * @param timescale
     * @param start
     * @param end
     * @returns {Array<TimeLabelModel>}
     */
    getTimeLine(timescale: string, start: string = null,
                end: string = null): Array<TimeLabelModel> {
        let allTL: Array<TimeLabelModel> =
            this.timeLables.getScaleTimelabels(timescale);
        if (start === null && end === null) {
            return allTL;
        } else {
            let filteredTL = [];
            let toAdd = false;
            for (let i = 0; i < allTL.length; i++) {
                if (!toAdd && allTL[i].getName() == start) {
                    toAdd = true;
                }
                if (toAdd) {
                    filteredTL.push(allTL[i]);
                    if (end !== null && allTL[i].getName() == end) {
                        break;
                    }
                }
            }
            return filteredTL;
        }
    }

    /**
     *
     * @param timescaleKey
     * @param variableKey
     * @param timeline
     * @returns {Array<PointValueModel>}
     */
    getPointsValue(timescaleKey: string, variableKey: string,
                   timeline: Array<string>): Array<PointValueModel> {

        let pointsValue = [];
        if (this.pointsValues.storage[timescaleKey]
            && this.pointsValues.storage[timescaleKey][variableKey]) {
            for (let i = 0; i < this.pointsValues.storage[timescaleKey][variableKey].length; i++) {
                let timestamp = this.pointsValues.storage[timescaleKey][variableKey][i]['timestamp'];
                if (timeline.indexOf(timestamp) != -1) { // TODO REFACTOR - WARNING ORDER IS IMPORTANT
                    pointsValue.push(this.pointsValues.storage[timescaleKey][variableKey][i]);
                }
            }
        }
        return pointsValue;
    }

    /**
     *
     * @param type
     * @returns {Array<VariableModel>}
     */
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

    /**
     *
     * @param varKey
     * @param start
     * @param end
     * @param timescale
     * @returns {any}
     */
    getGrowthRate(varKey: string, start: string,
                  end: string, timescale: string): number {
        try {
            for (let i = 0; i < this.grRates.storage[varKey].length; i++) {
                if (
                    this.grRates.storage[varKey][i].start == start
                    && this.grRates.storage[varKey][i].end == end
                    && this.grRates.storage[varKey][i].timescale == timescale
                ) {
                    return this.grRates.storage[varKey][i].value;
                }
            }
        } catch (e) {
            // TODO Implement query for server
            console.error('Have no growth rate for:', varKey, start, end);
            return null;
        }
    }

    /**
     *
     * @param timescale
     * @returns {number}
     */
    getTimeScaleLag(timescale: string): number {
        let ts = this.timeScales.getTimeScale(timescale);
        return (ts) ? ts.growth_lag : null;
    }

    /**
     *
     * @param timescale
     * @param full_name
     * @param lag
     * @returns {TimeLabelModel}
     */
    getPreviousTimeLabel(timescale: string, full_name: string,
                         lag: number): TimeLabelModel {
        // TODO Improove method
        let allTL: Array<TimeLabelModel> =
            this.timeLables.getScaleTimelabels(timescale);
        for (let i = allTL.length - 1; i >= 0; i--) {
            if (allTL[i].full_name == full_name) {
                if (allTL[i-lag]) {
                    return allTL[i-lag]
                } else {
                    break;
                }
            }
        }
        console.error('Have no prev period for:', timescale, full_name, lag);
        return null;
    }

    getTimeScalesOrder() {
        return this.timeScales.order;
    }

    getPlainTimeLabels(): Array<TimeLabelModel> {
        return this.timeLables.storage; // TODO Make right
    }

    getVariable(name: string): VariableModel {
        return this.variables.storage[name];
    }

    variableExists(varName: string): boolean {
        return (varName in this.variables.storage);
    }
}
