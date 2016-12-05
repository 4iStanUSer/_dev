import {WaterfallChartDataInput} from "../../common/cmp/waterfall-chart/waterfall-chart.component";
import {BarChartDataInput} from "../../common/cmp/bar-chart/bar-chart.component";
import {TableWidgetData} from "../../common/cmp/table-widget/table-widget.component";


/**
 * Data structure for showing Decomposition Waterfall (absolute and rate mode)
 * and row with changes under waterfall
 */
export interface DecompositionTypeData {
    abs: WaterfallChartDataInput;
    rate: WaterfallChartDataInput;
    table: Array<{
        name: string,
        value: number,
        metric: string
    }>;
}

/**
 * Data structure for showing variables tab(s) inside Forecast Section
 * in absolute or growth rate modes and CAGR block
 */
export interface VariableData {
    abs: BarChartDataInput,
    rate: Array<{
        name: string;
        value: number;
    }>,
    cagr?: Array<{
        start: string;
        end: string;
        value: number;
    }>
}

/**
 * Data structure for showing Table via TableWidget and storage of rows IDs
 */
export interface ClickableTable {
    data: TableWidgetData;
    rows_data: {
        [id: string]: {driver_key: string};
    }
}
