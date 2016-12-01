export type Point = (number | [number, number] | [string, number]
    | HighchartsDataPoint);
export type ChartSerie = HighchartsSeriesOptions;

/**
 * Stores configuration options for Highcharts
 * and is able to do some operations with the options.
 * It is used as input variable into Chart Directive.
 */
export class Chart {
    ref: HighchartsChartObject;

    constructor(public options: HighchartsOptions) {
        // init series array if not set
        if (!this.options.series) {
            this.options.series = [];
        }
    }

    addSerie(serie: ChartSerie): void {
        // init data array if not set
        if (!serie.data) {
            serie.data = [];
        }

        this.options.series.push(serie);

        if (this.ref) {
            this.ref.addSeries(serie);
        }
    }

    removeSerie(serieIndex: number): void {
        this.options.series.splice(serieIndex, 1);
        if (this.ref) {
            this.ref.series[serieIndex].remove(true);
        }
    }

    setData(): void {

    }

    // addPoint(point: Point, serieIndex = 0, redraw = true, shift = false): void {
    //     (<Point[]>this.options.series[serieIndex].data).push(point);
    //     if (this.ref) {
    //         this.ref.series[serieIndex].addPoint(point, redraw, shift);
    //     }
    // }
    //
    // removePoint(pointIndex: number, serieIndex = 0): void {
    //     // TODO add try catch (empty)
    //     (<Point[]>this.options.series[serieIndex].data).splice(pointIndex, 1);
    //     if (this.ref) {
    //         this.ref.series[serieIndex].removePoint(pointIndex, true);
    //     }
    // }
}
