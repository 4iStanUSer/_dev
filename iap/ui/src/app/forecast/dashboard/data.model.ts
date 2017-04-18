// Input Types
type TimescalesInput = Array<Timescale>;
type TimelablesInput = Array<Timelabel>;
type VariablesInput = Array<Variable>;
type DecompTypesInput = Array<DecompType>;

type VariableValuesInput = {
    [timescale_id: string]: {
        [variable_id: string]: {
            [timelable_id: string]: number; // TODO Question - maybe more
        }
    }
};
type ChangesOverPeriodInput = {
    [timescale_id: string]: {
        [variable_id: string]: Array<ChangeOverPeriod>;
    }
};

type DecompInput = {
    [timescale_id: string]: {
        [decomp_type_id: string]: Array<Decomposition>
    }
};
type DecompTypeFactorsInput = {
    [decomp_type_id: string]: Array<string>; // array of factors (variables) ID
};
type FactorDriversInput = {
    // variable_id === factor_id
    [variable_id: string]: Array<FactorDriver>
};


// - Single Item Types
type Timescale = {
    id: string;
    full_name: string;
    short_name: string;
    lag: number;
};

type Timelabel = {
    id: string;
    full_name: string;
    short_name: string;
    parent_index: number;
    timescale: string;
};

export type Variable = {
    id: string;
    full_name: string;
    short_name: string;
    type: string; // 'driver'|'output'|'decomp'
    metric: string;
    format: string;
    hint: string;
};

type DecompType = {
    id: string;
    full_name: string;
    short_name: string;
}

type ChangeOverPeriod = {
    start: string;
    end: string;
    abs: number;
    rate: number;
};

type Decomposition = {
    start: string;
    end: string;
    factors: Array<{
        var_id: string;
        abs: number;
        rate: number;
    }>
}

type FactorDriver = {
    factor: string; // variable_id
    driver: string; // variable_id
}


/**
 * Model of data for Dashboard Page.
 * It uses by DataManager (DashboardComponent's service)
 */
export class DashboardDataModel {
    timescales: TimescalesInput = null;
    timelables: TimelablesInput = null;
    vars: VariablesInput = null;
    varValues: VariableValuesInput = null;
    changes: ChangesOverPeriodInput = null;
    decompTypes: DecompTypesInput = null;
    decomp: DecompInput = null;
    factorDrivers: FactorDriversInput = null;
    decompTypeFactors: DecompTypeFactorsInput = null;

    constructor(timescales: TimescalesInput,
                timelables: TimelablesInput,
                variables: VariablesInput,
                variable_values: VariableValuesInput,
                change_over_period: ChangesOverPeriodInput,
                decomp_types: DecompTypesInput,
                decomp: DecompInput,
                factor_drivers: FactorDriversInput,
                decomp_type_factors: DecompTypeFactorsInput) {
        this.timescales = timescales;
        this.timelables = timelables;
        this.vars = variables;
        this.varValues = variable_values;
        this.changes = change_over_period;
        this.decompTypes = decomp_types;
        this.decomp = decomp;
        this.factorDrivers = factor_drivers;
        this.decompTypeFactors = decomp_type_factors;
    }


    /**
     * Returns array of Timelabels for timescale between start_timelabel_id
     * and end_timelabel_id.
     * If end_timelabel_id is not defined - returns array from start_timelabel
     * to end of timelabels list of timescale.
     * If start_timelabel_id is not defined too - returns full list
     * of timelabels for timescale!
     *
     * @param timescale_id
     * @param start_timelabel_id
     * @param end_timelabel_id
     * @returns {Array<Timelabel>}
     */
    getTimeLine(timescale_id: string,
                start_timelabel_id: string = null,
                end_timelabel_id: string = null): Array<Timelabel> {

        let allTL = this.getScaleTimelabels(timescale_id);
        if (start_timelabel_id === null && end_timelabel_id === null) {
            return allTL;
        } else {
            let filteredTL = [];
            let toAdd = false;
            for (let i = 0; i < allTL.length; i++) {
                if (!toAdd && allTL[i].id == start_timelabel_id) {
                    toAdd = true;
                }
                if (toAdd) {
                    filteredTL.push(allTL[i]);
                    if (end_timelabel_id !== null
                        && allTL[i].id == end_timelabel_id) {
                        break;
                    }
                }
            }
            return filteredTL;
        }
    }

    /**
     * Need to be removed
     * @param timescale_id
     * @returns {Array<Timelabel>}
     */
    getScaleTimelabels(timescale_id: string): Array<Timelabel> {
        // TODO Review - use this.getTimeLine()
        let l = (this.timelables && this.timelables.length)
            ? this.timelables.length : 0;
        let output = [];
        for (let i = 0; i < l; i++) {
            if (this.timelables[i].timescale == timescale_id) {
                output.push(this.timelables[i]);
            }
        }
        return output;
    }

    /**
     * Returns array of absolute values for variable(variable_id)
     * for timeline(timelabel_ids). Values are in same order as timelabels.
     * If there is not value for variable for timelabel - it pushes null
     * @param timescale_id
     * @param variable_id
     * @param timelabel_ids
     * @returns {Array<number>}
     */
    getPointsValue(timescale_id: string, variable_id: string,
                   timelabel_ids: Array<string>): Array<number> {

        let output = [];

        let l = (timelabel_ids && timelabel_ids.length)
            ? timelabel_ids.length : 0;
        console.log(l);
        for (let i = 0; i < l; i++) {
            try {
                let tl_id = timelabel_ids[i];
                //TODO Question update value structure from backend
                let val = this.varValues[timescale_id][variable_id]['values'][i];
                output.push(val);
            } catch (e) {
                output.push(null);
            }
        }
        return output;
    }

    /**
     * Returns parent Timelabel object, if there is not parent - returns null
     * @param timelabel_id
     * @param timescale_id
     * @returns {Timelabel}
     */
    getParentTimelabel(timelabel_id: string, timescale_id: string): Timelabel {
        let l = (this.timelables && this.timelables.length)
            ? this.timelables.length : 0;

        for (let i = 0; i < l; i++) {
            if (this.timelables[i].id == timelabel_id
                && this.timelables[i].timescale == timescale_id) {
                if (this.timelables[i].parent_index !== null
                    && this.timelables[this.timelables[i].parent_index]) {
                    return this.timelables[this.timelables[i].parent_index];
                } else {
                    break;
                }
            }
        }
        return null;
    }

    /**
     * Returns list of Variable objects, each of them has requested type
     * @param type
     * @returns {Array<Variable>}
     */
    getVariablesByType(type: string): Array<Variable> {
        let output = [];
        let l = (this.vars && this.vars.length) ? this.vars.length : 0;
        for (let i = 0; i < l; i++) {
            if (type == this.vars[i].type) {
                output.push(this.vars[i]);
            }
        }
        return output;
    }

    /**
     * Returns Growth Rate absolute value for requested variable and period
     * If there is not growth rate - returns null and push error into console
     * @param variable_id
     * @param start_timelabel_id
     * @param end_timelabel_id
     * @param timescale_id
     * @returns {number}
     */
    getGrowthRate(variable_id: string, start_timelabel_id: string,
                  end_timelabel_id: string, timescale_id: string): number {
        try {
            console.log("getGrowthRate", this.changes);
            let l = this.changes[timescale_id][variable_id].length;
            for (let i = 0; i < l; i++) {
                let change = this.changes[timescale_id][variable_id][i];
                if (
                    change.start == start_timelabel_id
                    && change.end == end_timelabel_id
                ) {
                    console.log("Growth Rate for",variable_id, start_timelabel_id, end_timelabel_id, change.abs);
                    return change.abs; // TODO Question: Absolute|Rate OR Update
                }
            }
        } catch (e) {
            console.error('Don\'t have ChangeOverPeriod:',
                variable_id, start_timelabel_id, end_timelabel_id);
            return null;
        }
    }

    /**
     * Returns count of time points to define previous period point.
     * @param timescale_id
     * @returns {number}
     */
    getTimeScaleLag(timescale_id: string): number { // TODO Maybe use getTimescale()
        let ts = this.getTimescale(timescale_id);
        return (ts) ? ts.lag : null;
    }

    /**
     * Returns Timescale object by timescale_id
     * @param timescale_id
     * @returns {Timescale}
     */
    getTimescale(timescale_id: string): Timescale {
        let l = (this.timescales && this.timescales.length)
            ? this.timescales.length : 0;
        for (let i = 0; i < l; i++) {
            if (this.timescales[i].id == timescale_id) {
                return this.timescales[i];
            }
        }
        return null;
    }

    /**
     * Returns previous sibling timelabel (in the same timescale)
     * @param timescale_id
     * @param timelabel_id
     * @param lag
     * @returns {Timelabel}
     */
    getPreviousTimeLabel(timescale_id: string, timelabel_id: string,
                         lag: number): Timelabel {

        let allTL = this.getScaleTimelabels(timescale_id);
        for (let i = allTL.length - 1; i >= 0; i--) {
            if (allTL[i].id == timelabel_id) {
                if (allTL[i - lag]) {
                    return allTL[i - lag]
                } else {
                    break;
                }
            }
        }
        //console.error('Don\'t have previous period for:',
        //    timescale_id, timelabel_id, lag);
        return null;
    }

    /**
     * Returns list of timescales with hierarchical order
     * @returns {string[]|Array}
     */
    getTimeScalesOrder(): Array<string> {
        return (this.timescales && this.timescales.length)
            ? this.timescales.map((ts: Timescale) => {
            return ts.id;
        }) : [];
    }

    /**
     * Returns list of decomposition types
     * @returns {string[]|Array}
     */
    getDecompositionTypes(): Array<string> {
        return (this.decompTypes && this.decompTypes.length)
            ? this.decompTypes.map((dt: DecompType) => {
            return dt.id;
        }) : [];
    }

    /**
     * Returns decomposition data for type, start and end timelabels.
     * If there is not data for specified period - returns null
     * @param decomp_type_id
     * @param timescale_id
     * @param start
     * @param end
     * @returns {Decomposition}
     */
    getDecomposition(decomp_type_id: string,
                     timescale_id: string,
                     start: string,
                     end: string): Decomposition {
        try {
            let l = this.decomp[timescale_id][decomp_type_id].length;
            for (let i = 0; i < l; i++) {
                if (this.decomp[timescale_id][decomp_type_id][i].start == start
                    &&
                    this.decomp[timescale_id][decomp_type_id][i].end == end) {
                    return this.decomp[timescale_id][decomp_type_id][i];
                }
            }
        } catch (e) {
            console.error('Don\'t have decomposition data for:',
                timescale_id, decomp_type_id, start, end);
        }
        return null;
    }

    /**
     * Returns Variable object by variable_id
     * @param variable_id
     * @returns {Variable}
     */
    getVariable(variable_id: string): Variable {
        let l = (this.vars && this.vars.length) ? this.vars.length : 0;
        for (let i = 0; i < l; i++) {
            if (variable_id == this.vars[i].id) {
                return this.vars[i];
            }
        }
        return null;
    }

    /**
     * Returns list of factors (variable_id) for decomposition type
     * @param decomp_type_id
     * @returns {Array<string>}
     */
    getDecompTypeFactors(decomp_type_id: string): Array<string> {
        return (this.decompTypeFactors
        && this.decompTypeFactors[decomp_type_id])
            ? this.decompTypeFactors[decomp_type_id] : null;
    }

    /**
     * Returns list of drivers (variable_id) for factor
     * @param factorId
     * @returns {Array<string>}
     */
    getFactorDrivers(factorId: string): Array<string> {
        if (this.factorDrivers && this.factorDrivers[factorId]) {
            return this.factorDrivers[factorId].map((item) => {
                return item['driver'];
            })
        }
        return null;
    }

    /**
     * Returns related factor (variable_id) for impact section
     * If null data is passed, or not found related factor,
     * or found more than one - returns null
     * @param factorId
     * @param driverId
     * @returns {string}
     */
    getRelatedFactor(factorId: string, driverId: string): string {
        if (!factorId || !driverId)
            return null;
        else {
            let output = null;
            try {
                let factorsByDriver = this.factorDrivers[factorId]
                    .filter(function (el) {
                        return (el['driver'] === driverId);
                    });
                if (factorsByDriver.length == 1) {
                    output = factorsByDriver[0]['factor'];
                } else if (factorsByDriver.length > 1) {
                    console.error('More than one related factor');
                } else {
                    console.error('Related factor not found');
                }
            }
            catch (e) { }
            return output;
        }
    }

    /**
     * Check if there is decomposition data for requested period.
     * Check this in first decomposition type's data in specified timescale
     * @param timescale
     * @param start
     * @param end
     * @returns {boolean}
     */
    hasDecomposition(timescale: string, start: string, end: string): boolean {
        // TODO Optimize method
        if (this.decomp && this.decomp[timescale]) {
            let types = Object.keys(this.decomp[timescale]);
            if (types.length) {
                let l = this.decomp[timescale][types[0]].length;
                for (let i = 0; i < l; i++) {
                    let dec = this.decomp[timescale][types[0]][i];
                    if (dec.start == start && dec.end == end) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /**
     * Check if there is changes over period for requested period.
     * Check this in first variable's data in specified timescale
     * @param timescale
     * @param start
     * @param end
     * @returns {boolean}
     */
    hasChangesOverPeriod(timescale: string, start: string,
                         end: string): boolean {
        // TODO Optimize method
        if (this.changes && this.changes[timescale]) {
            let vars = Object.keys(this.changes[timescale]);
            if (vars.length) {
                let l = this.changes[timescale][vars[0]].length;
                for (let i = 0; i < l; i++) {
                    let change = this.changes[timescale][vars[0]][i];
                    if (change.start == start && change.end == end) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /**
     * Adds set of data into decomposition storage. Old data keeps.
     * @param decomp
     */
    addDecomposition(decomp: DecompInput): void {
        // TODO Check .merge() method
        // TODO Check for duplicate
        if (!this.decomp) {
            this.decomp = {};
        }
        let timescales = Object.keys(decomp);
        for (let i = 0; i < timescales.length; i++) {
            let ts = timescales[i];
            if (!this.decomp[ts]) {
                this.decomp[ts] = {};
            }
            let types = Object.keys(decomp[ts]);
            for (let j = 0; j < types.length; j++) {
                let type = types[j];
                if (!this.decomp[ts][type]) {
                    this.decomp[ts][type] = [];
                }
                this.decomp[ts][type] = this.decomp[ts][type]
                    .concat(decomp[ts][type]);
            }
        }
    }

    /**
     * Adds set of data into changes storage. Old data keeps.
     * @param decomp
     */
    addChangesOverPeriod(changes: ChangesOverPeriodInput) {
        // TODO Check .merge() method
        // TODO Check for duplicate
        if (!this.changes) {
            this.changes = {};
        }
        let timescales = Object.keys(changes);
        for (let i = 0; i < timescales.length; i++) {
            let ts = timescales[i];
            if (!this.changes[ts]) {
                this.changes[ts] = {};
            }
            let vars = Object.keys(changes[ts]);
            for (let j = 0; j < vars.length; j++) {
                let variable_id = vars[j];
                if (!this.changes[ts][variable_id]) {
                    this.changes[ts][variable_id] = [];
                }
                this.changes[ts][variable_id] = this.changes[ts][variable_id]
                    .concat(changes[ts][variable_id]);
            }
        }
    }
}
