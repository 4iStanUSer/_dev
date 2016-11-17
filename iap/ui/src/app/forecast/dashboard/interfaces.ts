import {WaterfallChartDataInput} from "../../common/cmp/waterfall-chart/waterfall-chart.component";
import {BarChartDataInput} from "../../common/cmp/bar-chart/bar-chart.component";
import {TableWidgetData} from "../../common/cmp/table-widget/table-widget.component";


export interface DecompositionTypeData {
    abs: WaterfallChartDataInput;
    rate: WaterfallChartDataInput;
    table: Array<{
        name: string,
        value: number,
        metric: string
    }>;
}

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
export interface ClickableTable {
    data: TableWidgetData;
    rows_data: {
        [id: string]: {driver_key: string};
    }
}
