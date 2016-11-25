/*
 INPUT VARIABLES:
 timescales:
 [{
 id:'',
 full_name:'',
 short_name:'',
 lag:''
 }]

 timelables:
 [{
 id:'',
 full_name:'',
 short_name:'',
 parent_index:'',
 timescale:''
 }]

 variables:
 [{
 id:'',
 full_name:'',
 short_name:'',
 type:'driver'|'output'|'decomp',
 metric:'',
 format:'',
 hint:''
 }]

 variable_values:
 {
 timescale_id: {
 var_id: {
 timelable_id: ''
 }
 }
 }

 change_over_period: {
 timescale_id: {
 var_id: [{
 start:'',
 end: '',
 abs: '',
 rate: ''
 }]
 }
 }

 decomp_types: [{
 id:'',
 full_name:'',
 short_name:''
 }]

 decomp: {
 timescale_id: {
 decomp_type_id:[{
 start: '',
 end: '',
 factors: [{
 var_id: '',
 abs: '',
 rate: ''
 }]
 }]
 }
 }
 factor_drivers: {
 var_id (factor_id): [{
 factor: var_id,
 driver: var_id
 }]
 }

 * */


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
                decomp_type_factors: DecompTypeFactorsInput
    ) {
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


    /*=====NEW REALIZATION====*/
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

    getScaleTimelabels(timescale_id: string): Array<Timelabel> {
        // TODO Review
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

    getPointsValue(timescale_id: string, variable_id: string,
                   timelabel_ids: Array<string>): Array<number> {

        let output = [];
        let l = (timelabel_ids && timelabel_ids.length)
            ? timelabel_ids.length : 0;
        for (let i = 0; i < l; i++) {
            try {
                let tl_id = timelabel_ids[i];
                let val = this.varValues[timescale_id][variable_id][tl_id];
                output.push(val);
            } catch (e) {
                output.push(null);
            }
        }
        return output;
    }

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

    getGrowthRate(variable_id: string, start_timelabel_id: string,
                  end_timelabel_id: string, timescale_id: string): number {
        try {
            let l = this.changes[timescale_id][variable_id].length;
            for (let i = 0; i < l; i++) {
                let change = this.changes[timescale_id][variable_id][i];
                if (
                    change.start == start_timelabel_id
                    && change.end == end_timelabel_id
                ) {
                    return change.abs; // TODO Question: Absolute|Rate
                }
            }
        } catch (e) {
            // TODO Implement query to server
            console.error('Don\'t have ChangeOverPeriod:',
                variable_id, start_timelabel_id, end_timelabel_id);
            return null;
        }
    }

    getTimeScaleLag(timescale_id: string): number { // TODO Maybe use getTimescale()
        let ts = this.getTimescale(timescale_id);
        return (ts) ? ts.lag : null;
    }

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
        console.error('Don\'t have previous period for:',
            timescale_id, timelabel_id, lag);
        return null;
    }

    getTimeScalesOrder(): Array<string> {
        return (this.timescales && this.timescales.length)
            ? this.timescales.map((ts: Timescale) => {
                return ts.id;
            }) : [];
    }

    getDecompositionTypes(): Array<string> {
        return (this.decompTypes && this.decompTypes.length)
            ? this.decompTypes.map((dt: DecompType) => {
                return dt.id;
            }) : [];
    }

    hasDecomposition(start_timelabel_id: string,
                     end_timelabel_id: string): boolean { // TODO Check type
        return true;
        // let l = this.storage.length;
        // for (let i = 0; i < l; i++) {
        //     if (this.storage[i].start == start_timelabel_id
        //         && this.storage[i].end == end_timelabel_id) {
        //         return true;
        //     }
        // }
        // return false;
    }

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
        } catch(e) { }
        return null;
    }

    getVariable(variable_id: string): Variable {
        let l = (this.vars && this.vars.length) ? this.vars.length : 0;
        for (let i = 0; i< l;i++) {
            if (variable_id == this.vars[i].id) {
                return this.vars[i];
            }
        }
        return null;
    }

    getDecompTypeFactors(decomp_type_id: string): Array<string> {
        return (this.decompTypeFactors
            && this.decompTypeFactors[decomp_type_id])
            ? this.decompTypeFactors[decomp_type_id] : null;
    }

    getFactorDrivers(factorId: string): Array<string> {
        if (this.factorDrivers && this.factorDrivers[factorId]) {
            return this.factorDrivers[factorId].map((item) => {
                return item['driver'];
            })
        }
        return null;
    }
    getRelatedFactor(factorId: string, driverId: string): string {
        if(!factorId || !driverId)
            return null;
        else{
            let output = '';
            try{
                let factorsByDriver = this.factorDrivers[factorId].filter(function (el) {
                    return (el['driver'] === driverId);
                });
                //TODO find out if it is ok to use [0] and if checking for arr length is needed factorsByDriver.len must be equal to 1
                output = factorsByDriver[0]['factor'];
            }
            catch (e) {
                console.error('Related factor not found');
                output = null;
            }

            return output;
        }
    }
}
