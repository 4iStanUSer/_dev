import {Component, OnInit} from '@angular/core';
import {Location} from '@angular/common';

@Component({
    selector: 'dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
    private blockView: Array<boolean> = [
        false,
        false
    ];

    private donuts: Array<Object> = [
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

    private bars: Array<Object> = [
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

    private waterfall: Object = {
        name: 'Decomposition 2015-2020',
        pipsName: '%',
        data: [
            {
                name: '2015',
                value: 100
            }, {
                name: 'Economy',
                value: 10
            }, {
                name: 'Demographic',
                value: 12
            }, {
                name: 'Inflation',
                value: 15
            }, {
                name: 'Distribution',
                value: 4
            }, {
                name: 'Pricing',
                value: -5
            }, {
                name: '2020'
            }
        ]
    };

    constructor(private _location: Location) {
    }

    ngOnInit() {
    }

    private changedBlockView(index, value) {
        this.blockView[index] = value;
        let path = this._location.path();
        console.log(path);
        // this._location.go(path, 'a=1');

        // let params = new URLSearchParams();
        // params.set('first_block', (this.blockView[index])?'1':'0');
        // console.log();
        // console.log(event);
    }

}
