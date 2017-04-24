import {Component, OnInit, Input } from '@angular/core';


@Component({
    selector: 'line-chart',
    templateUrl: './line-chart.component.html',
    styleUrls: ['./line-chart.component.css']
})

export class LineChartComponent {

    /*private chartConfig: Object = {
      chart: {
        renderTo: container,
        className: 'line-compare',
        spacingLeft: spacingLeft,
        spacingBottom: 0,
        events: {
          render: function() {
           this.yAxis[0].removePlotBandOrLine();
            max = this.yAxis[0].max;
            min = this.yAxis[0].min;
            mid = Math.round((max + min) / 2);
            maxText = max;
            minText = min;
            midText = Math.round((maxText + minText) / 2);
            this.yAxis[0].addPlotLine({
              value: max,
              color: config.colors.gridLines,
              dashStyle: 'dot',
              width: 1,
              label: {
                align: 'left',
                text: '$ ' + maxText,
                style: {
                  fontSize: plotLinesFont,
                  color: config.colors.text,
                },
                x: -spacingLeft,
                y: 4
              }
            });
            this.yAxis[0].addPlotLine({
              value: mid,
              color: config.colors.gridLines,
              dashStyle: 'dot',
              width: 1,
              label: {
                align: 'left',
                text: '$ ' + mid,
                style: {
                  fontSize: plotLinesFont,
                  color: config.colors.text,
                },
                x: -spacingLeft,
                y: 4
              }
            });
            this.yAxis[0].addPlotLine({
              value: min,
              color: config.colors.gridLines,
              dashStyle: 'dot',
              width: 1,
              label: {
                align: 'left',
                text: '$ ' + minText,
                style: {
                  fontSize: plotLinesFont,
                  color: config.colors.text,
                },
                x: -spacingLeft,
                y: 4
              }
            });
            this.navigator.yAxis.addPlotLine({
              value: this.navigator.yAxis.min + 2,
              color: config.colors.gridLines,
              dashStyle: 'dot',
              width: 1
            });
          }
        }
      },
      rangeSelector: {
        enabled: false
      },
      title: {
        text: '',
      },
      xAxis: {
        tickLength: 0,
        lineColor: 'transparent',
        max: config.rangeEnd,
        min: config.rangeBegin,
        //  range: config.range,
        labels: {
          enabled: false
        }
      },
      yAxis: {
        gridLineWidth: 0,
        opposite: false,
        showLastLabel: true,
        labels: {
          enabled: false
        },
      },
      credits: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      scrollbar: {
        enabled: false
      },
      legend: {
        enabled: true,
        align: 'left',
        padding: 10,
        itemDistance: legendItemMargin,
        itemStyle: {
          width: 90,
          fontSize: 10,
          color: config.colors.text
        },
        symbolWidth: 20,
        width: 300,
        y: 1,
        x: -10
      },
      navigator: {
        maskInside: false,
        height: navigatorHeight,
        margin: navigatorMargin,
        maskFill: maskFill,
        xAxis: {
          tickWidth: 0,
          lineWidth: 0,
          tickInterval: 30 * 24 * 3600 * 1000,
          gridLineWidth: 0,
          startOnTick: true,
          showFirstLabel: true,
          endOnTick: true,
          labels: {
            step: 2,
            align: 'left',
            style: {
                fontSize: plotLinesFont,
                color: config.colors.text
            },
            x: 3,
            y: 15
          }
        },
        series: {
          type: 'areaspline',
          color: config.colors.navigator,

          fillColor : {
            linearGradient : [0, 0, 0, 300],
            stops : [
              [0, Highcharts.Color(config.colors.navigator).setOpacity(gradientOpacity).get('rgba')],
              [0.1, Highcharts.Color('#ffffff').setOpacity(0).get('rgba')],
              [1, Highcharts.Color('#ffffff').setOpacity(0).get('rgba')]
            ]
          }
        }
      },
      plotOptions: {
        series: {
          enableMouseTracking: false,
          states: {
            hover: {
              enabled: false
            }
          }
        },
        line: {
          marker: {
            enabled: false
          }
        }
      },
      series: [{
        name: config.lineName,
        color: config.colors.line,
        data: data
      }, {
        name: config.lineName2,
        color: config.colors.line2,
        data: data2
      }]
    }
    */
    constructor() {}

}
