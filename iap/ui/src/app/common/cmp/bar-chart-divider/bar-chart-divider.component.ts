import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Chart} from './../../module/chart/';


export type BarChartDataInput = Array<{
    name: string;
    value: number;
}>;

@Component({
    selector: 'bar-chart-divider',
    templateUrl: './bar-chart-divider.component.html',
    styleUrls: ['bar-chart-divider.component.css']
})
/**
 * Simple wrapper component for Bars Chart.
 * http://www.highcharts.com/demo/column-basic
 * Main aim - configure chart options, process/transform input data
 * for using inside Highcharts library.
 * Should be used inside template of page/tab components
 */
export class BarChartDividerComponent implements OnInit {

    private chart: Chart = null;
    private maxRate = 90;
    private gridLines = '#c3cad6';
    private chartConfig: Object = {
      chart: {
        type: 'column',
        className: 'gistogram-divider',

        /**events: {

          redraw: function () {
            console.log();
            this.borderElement = this.helper.drawBordersPlotCompare(this, this.config, spacing, pointWidth, this.borderElement);
            this.helper.correctLabelsPos(this, this.config, growingLabelWidth);
            this.hideFirstLabel(this.config.container);
            centerFirstLabel(this.series[1].data, this.config.container);
          },
          load: function(event) {
            $('.highcharts-legend-item rect').attr('height', '2').attr('y', '10');
            $('.highcharts-legend-item rect').attr('width', '25').attr('x', '-20');
          }

        },
        */
        marginLeft: 4,
        marginRight: 4,
        spacingTop: 20,
        spacingBottom: 0
      },
      title: {
        text: null
      },
      xAxis: {
        tickLength: 0,
        lineColor: 'transparent',
        type: 'category',
        labels: {
          step: 1,
          useHTML: true,
          y: 15,
          style: {
            color: "#888e95",
          },
        }
      },
      yAxis: {
        gridLineWidth: 0,
        maxPadding: 0,
        plotLines: [{
          value: this.maxRate,
          color: this.gridLines,
          dashStyle: 'dot',
          width: 1
        },{
          value: this.maxRate/ 2,
          color: this.gridLines,
          dashStyle: 'dot',
          width: 1,
        },{
          value: 0,
          color: this.gridLines,
          dashStyle: 'dot',
          width: 1,
        }],
        labels: {
          enabled: false
        }
      },
      legend: {
        align: 'left',
        padding: 7,
        itemDistance: 50,
        itemStyle: {
          width: 90,
          fontSize: 10,
          color: "#ecf0f7"
        },
        symbolWidth: 4,
        width: 300
      },
      credits: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      plotOptions: {
        column: {
          stacking: 'normal',
          groupPadding: 0.1
        },
        series: {
          dataLabels: {
            allowOverlap: true
          },
          events: {
            legendItemClick: function () {
                return false;
            }
          }
        },
        allowPointSelect: false,
      },
      series: [
        {
          name: 'background',
          showInLegend: false,
          stack: 0,
          className: 'column-background',
          type: 'column',
          states: {
            hover: {
              enabled: false
            }
          },
          color: '#f1a94e',
          pointWidth: 19,
          borderRadiusTopRight: 5,
          borderRadiusTopLeft: 5,
          borderWidth: 0,
          data: []
        }, {
          name: "simulation",
          stack: 0,
          type: 'column',
          color: '#e45641',
          pointWidth: 19,
          borderWidth: 0,
          borderRadiusBottomRight: 5,
          borderRadiusBottomLeft: 5,
          data: [],
          dataLabels: {
            enabled: true,
            inside: false,
            y: 4,
            style: {
              fontSize: '12px',
              fontFamily: 'open_sanssemibold',
              color: "#ecf0f7"
            }
          }
        }, {
          name: "Baseline scenario",
          stack: 1,
          type: 'column',
          color: "#ff8080",
          pointWidth: 19,
          borderWidth: 0,
          borderRadiusBottomRight: 5,
          borderRadiusBottomLeft: 5,
          data: [],
          dataLabels: {
            enabled: true,
            inside: false,
            y: 4,
            style: {
              fontSize: '12px',
              fontFamily: 'open_sanssemibold',
              color: "#ff8080"
            }
          }
        }
      ]
    };
    private helper;
    @Input() set data(data: BarChartDataInput) {
        console.info('BarChartDividerComponent: set data');
        console.log(data);
        let dataToPush = [];
        for (let i = 0; i < data.length; i++) {
            dataToPush.push([
                data[i]['name'].toString(),
                data[i]['value']
            ]);
        }
        this.chartConfig['series'][0]['data'] = dataToPush[1];
        this.chartConfig['series'][1]['data'] = dataToPush;
        this.chartConfig['series'][2]['data'] = dataToPush;
        this.chart = new Chart(this.chartConfig)
    };

    constructor() {
    }


    ngOnInit() {

    }
}
