import {Component, OnInit, Input, Output, EventEmitter, ElementRef, Renderer} from '@angular/core';
import * as _ from 'lodash';

//import * as moment from 'moment';
//const TODAY2: Date =
//const TODAY: Date = new Date(TODAY2.getFullYear(), TODAY2.getMonth(), TODAY2.getDate(),0,0,0,0);

@Component({
    selector: 'datepicker',
    templateUrl: 'datepicker.component.html',
    styleUrls: ['datepicker.component.css']

})
export class DatepickerComponent implements OnInit {
    @Input() date: string;
    @Output() dateChanged = new EventEmitter();
    private bodyClickListener: Function = null;

    public constructor(private elRef: ElementRef, private rndr: Renderer) { }

    private toHideCalendar(e: Event = null) {
        console.log('toHideCalendar');
        this.showCalendar = false;
        if (this.bodyClickListener != null) {
            this.bodyClickListener();
            this.bodyClickListener = null;
        }
    }
    private toShowCalendar(e: Event = null) {
        console.log('toShowCalendar');
        this.showCalendar = true;
        if (this.bodyClickListener == null) {
            this.bodyClickListener = this.rndr.listenGlobal(
                'document', 'click', (event) => {
                    if (!this.elRef.nativeElement.contains(event.target)
                        && event.target.getAttribute('id') != 'show_months_grid'
                        && !event.target.classList.contains('month-item')) {

                        this.toHideCalendar();
                        console.log('event.target.classList', event.target.classList);
                    }
                });
        }
    }

    public _today: Date = new Date();
    public dateFormat: string = 'dd/mm/yyyy';
    public _activeDate: Date = _.cloneDeep(this._today);
    public selectedDate: Date = _.cloneDeep(this._today);
    public niceSelectedDate: string;
    public weekDay: number = this._activeDate.getDay();
    public weekArr: Array<string> = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
    public todayWeekName: string = this.weekArr[this.weekDay];

    public monthArr: Array<string> = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];
    public todayMonthName: string = this.monthArr[this._activeDate.getMonth()];


    public firstDayOfMonth: Date;
    public firstDate: Date;
    public datesArr: Array<Date>;

    public dateObjArr: Array<any>;
    public daysRows: Array<any>;

    public dateInputError: string = '';


    public viewState: string = 'dayGrid'; //monthGrid
    public monthsRows: Array<any>;

    public showCalendar: boolean = false;

    public ngOnInit(): void {

        this.firstDayOfMonth = new Date(this._activeDate.getFullYear(), this._activeDate.getMonth(), 1);
        this.buildCalendar(this.firstDayOfMonth);

        this.niceSelectedDate = this.format(this.selectedDate, this.dateFormat);
    }
    public buildCalendar(firstDayOfMonth: Date): void {
        this.firstDate = this.getFirstDateToShow(firstDayOfMonth);
        this.datesArr= this.getDates(this.firstDate, 42);
        this.dateObjArr = this.createDateObj(this.datesArr, this._activeDate);
        this.daysRows = this.getRows(this.dateObjArr);
    }

    private getActiveDate(): Date {
        return this._activeDate || this._today;
    }

    private setActiveDate(value: Date):void {
        this._activeDate = value;
    }

    private getDates(startDate: Date, n: number): Array<Date> {
        let dates: Array<Date> = new Array(n);
        let current = new Date(startDate.getTime());
        let i = 0;
        let date: Date;
        while (i < n) {
            date = new Date(current.getTime());
            dates[i++] = date;
            current = new Date(current.getFullYear(), current.getMonth(), current.getDate() + 1);
        }
        return dates;
    }

    private createDateObj(dates: Array<Date>, activeDate:Date): Array<any> {
        let dateObjArr: Array<any> = [];
        let dateObj: [Date, string, string]; //Tuple
        let i = 0;
        let len = dates.length;
        let id: string = '';
        let className:string = '';
        for (i = 0; i < len; ++i) {
            id = this.getElemId(dates[i]);
            if (dates[i].getMonth() == activeDate.getMonth()) {

                className = "info";
                if (dates[i].getMonth() == this.selectedDate.getMonth()
                    && dates[i].getDate() == this.selectedDate.getDate()
                    && dates[i].getFullYear() == this.selectedDate.getFullYear()) {
                    className = "primary";
                }
            } else {
                className = "secondary";
            }

            dateObj = [dates[i], className, id];
            dateObjArr.push(dateObj);
        }
        return dateObjArr;
    }
    private getRows(dateObjs: Array<any>): Array<any> {
        let rows: Array<any> = [];
        let i = 0;
        let chunkSize = 7;
        let len = dateObjs.length;
        for (i = 0; i < len; i += chunkSize) {
            rows.push(dateObjs.slice(i, i + chunkSize));
        }
        return rows;
    }
    private getFirstDateToShow(firstDayOfMonth: Date): Date {
        let difference = 0 - firstDayOfMonth.getDay();
        let numDisplayedFromPreviousMonth = (difference > 0)
        ? 7 - difference
            : -difference;
        let firstDate = new Date(firstDayOfMonth.getTime());
        if (numDisplayedFromPreviousMonth > 0) {
            firstDate.setDate(-numDisplayedFromPreviousMonth + 1);
        }
        return firstDate;
    }

    public getElemId(date: Date): string {
        let id: string = "" + date.getDate() + "" + date.getMonth() + "" + date.getFullYear() + "";
        return id;
    }

    public changeMonthUp(): void {
        let newMonth: number = this._activeDate.getMonth() + 1;
        let newDate: Date = _.cloneDeep(this._activeDate);
        newDate.setDate(1);
        newDate.setMonth(newMonth);
        this.setActiveDate(newDate);
        this.firstDayOfMonth.setMonth(newMonth);
        this.buildCalendar(this.firstDayOfMonth);
        this.dateInputError = '';
    }

    public changeMonthDown(): void {
        let newMonth: number = this._activeDate.getMonth() - 1;
        let newDate: Date = _.cloneDeep(this._activeDate);
        newDate.setDate(1);
        newDate.setMonth(newMonth);
        this.setActiveDate(newDate);
        this.firstDayOfMonth.setMonth(newMonth);
        this.buildCalendar(this.firstDayOfMonth);
        this.dateInputError = '';
    }


    public format(date: Date, format: string): string {
        let stripChar: string = format.replace(/\w/g, '').charAt(0);

        let dateNum: number = date.getDate();
        let dateStr: string = '' + dateNum;
        let fullDateStr: string = dateStr.length < 2 ? '0' + dateStr : dateStr;

        let monthNum: number = date.getMonth() + 1;
        let monthStr: string = '' + monthNum;
        let fullMonthStr: string = monthStr.length < 2 ? '0' + monthStr : monthStr;

        let niceDate: string = fullDateStr + stripChar + fullMonthStr + stripChar + date.getFullYear();
        return niceDate;
    }

    onKey(event: any) {
        let v = event.target.value;
        let dateArr: Array<string>;
        let dateFromInput: Date;
        if (v.length == 10) {
            let isValidDate = /^(0[1-9]|1\d|2\d|3[01])\/(0[1-9]|1[0-2])\/(19|20)\d{2}$/.test(v);
            if (isValidDate) {
                dateArr = v.split("/");
                let day = Number(dateArr[0]);
                let month = Number(dateArr[1]) - 1;
                let year = Number(dateArr[2]);
                if (this.isValidDay(year, month, day)) {
                    dateFromInput = new Date(year, month, day);
                    this._activeDate = _.cloneDeep(dateFromInput);
                    this.selectedDate = _.cloneDeep(dateFromInput);
                    this.niceSelectedDate = this.format(this.selectedDate, this.dateFormat);

                    this.firstDayOfMonth.setMonth(month);
                    this.firstDayOfMonth.setFullYear(year);

                    this.buildCalendar(this.firstDayOfMonth);
                    this.dateInputError = '';
                } else {
                    this.dateInputError = 'That month has less days';
                }
            } else {
                this.dateInputError = 'Invalid Date';
            }
        } else {
            this.dateInputError = 'Date is too short';
        }
    }
    public isValidDay(year: number, month: number, day: number): boolean {
        let daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        if ((!(year % 4) && year % 100) || !(year % 400)) {
            daysInMonth[1] = 29;
        }
        // If evenly divisible by 4 and not evenly divisible by 100,
        // or is evenly divisible by 400, then a leap year
        return day <= daysInMonth[month]
    }

    public showMonthsGrid(): void {
        this.viewState = 'monthGrid';
        this.buildMonthsGrid(this._activeDate);
    }


    public buildMonthsGrid(activeDate: Date): void {

        let monthsAmount:number = 12;
        let firstMonth: Date = new Date(activeDate.getFullYear(), 0, 1);

        let date: Date;
        let monthDatesArr: Array<Date> = new Array(monthsAmount);
        let count = 0;
        let current: Date = _.cloneDeep(firstMonth);
        while (count < monthsAmount) {
            date = new Date(current.getTime());
            monthDatesArr[count++] = date;
            current = new Date(current.getFullYear(), current.getMonth() + 1, current.getDate());
        }
        let i = 0;
        let chunk = 4;
        let monthObjArr: Array<any> = [];
        let monthObj: [Date, string, string, string]; //Tuple

        let longName: string = '';
        let id: string = '';
        let className: string = '';
        let shortName: string = '';


        let row: Array<any> = [];

        for (let dateIter of monthDatesArr) {
            id = this.getElemId(dateIter);
            className = "info";
            if (dateIter.getMonth() == this.selectedDate.getMonth()
                && dateIter.getFullYear() == this.selectedDate.getFullYear()) {
                className = "primary";
            }
            longName = this.monthArr[dateIter.getMonth()];
            shortName = longName.substr(0, 3);
            monthObj = [dateIter, className, id, shortName];
            monthObjArr.push(monthObj);
            i++;
            if (i % chunk == 0) {
                row.push(monthObjArr);
                monthObjArr = [];
            }
        }
        this.monthsRows = row;
    }

    public changeYearUp(): void {
        let newYear: number = this._activeDate.getFullYear() + 1;
        let newDate: Date = _.cloneDeep(this._activeDate);
        newDate.setDate(1);
        newDate.setFullYear(newYear);
        this.setActiveDate(newDate);
        this.buildMonthsGrid(newDate);
        this.dateInputError = '';
    }
    public changeYearDown(): void {
        let newYear: number = this._activeDate.getFullYear()- 1;
        let newDate: Date = _.cloneDeep(this._activeDate);
        newDate.setDate(1);
        newDate.setFullYear(newYear);
        this.setActiveDate(newDate);
        this.showMonthsGrid();
        this.dateInputError = '';
    }

    public changeDate(newDate: Date): void {

        this._activeDate = _.cloneDeep(newDate);
        this.selectedDate = _.cloneDeep(newDate);

        this.firstDayOfMonth.setMonth(newDate.getMonth());
        this.firstDayOfMonth.setFullYear(newDate.getFullYear());

        this.buildCalendar(this.firstDayOfMonth);
		this.niceSelectedDate = this.format(this.selectedDate, this.dateFormat);
        this.toHideCalendar();

        this.viewState = 'dayGrid';
        this.dateInputError = '';
    }

    public changeSelectedMonth(newDate: Date): void {
        this._activeDate = _.cloneDeep(newDate);

        this.firstDayOfMonth.setMonth(newDate.getMonth());
        this.firstDayOfMonth.setFullYear(newDate.getFullYear());

        this.buildCalendar(this.firstDayOfMonth);

        this.viewState = 'dayGrid';
        this.dateInputError = '';
    }
}


