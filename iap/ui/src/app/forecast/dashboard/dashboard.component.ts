import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    private donuts:Array<Object> = [
        {
            name: 'One',
            value: 86
        },
        {
            name: 'Two',
            value: 35
        },
        {
            name: 'Three',
            value: 49
        }
    ];

    private bars:Array<Object> = [
        {
            name: 'Sales, $ MM',
            data: [
                {
                    name: '2013',
                    value: 14.2
                },
                {
                    name: '2015',
                    value: 16.1
                },
                {
                    name: '2020F',
                    value: 23.7
                }
            ]
        },
        {
            name: 'Volume, EQ Thousands',
            data: [
                {
                    name: '2013',
                    value: 12.2
                },
                {
                    name: '2015',
                    value: 18.1
                },
                {
                    name: '2020F',
                    value: 33.7
                }
            ]
        },
        {
            name: 'Price – per EQ, $',
            data: [
                {
                    name: '2013',
                    value: 0.05
                },
                {
                    name: '2015',
                    value: 0.06
                },
                {
                    name: '2020F',
                    value: 0.08
                }
            ]
        },
    ];

    private waterfall = [];

    constructor() {
    }

    ngOnInit() {
    }

}
