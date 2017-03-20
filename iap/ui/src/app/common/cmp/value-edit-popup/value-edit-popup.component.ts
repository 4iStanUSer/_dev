import {Component, OnChanges, SimpleChanges, Input, Output, EventEmitter} from '@angular/core';


export interface PopupData {
  coordinate_x: number;
  coordinate_y: number;
  value: number;
  type_value: string;
  abs_format: string;
  percent_format: string;
  type_popup: string;
  absolute_step: number;
  percent_step: number;
  default_value: number;
}

@Component({
  selector: 'app-value-edit-popup',
  templateUrl: './value-edit-popup.component.html',
  styleUrls: ['./value-edit-popup.component.css']
})

export class ValueEditPopupComponent implements OnChanges {
    @Input() inputData:PopupData; // data from parent component
    @Output() popupRequest = new EventEmitter<number>();

    private lang = {
        'apply': 'Apply',
        'cancel': 'Cancel',
        'reset': 'Reset to Default',
        'increase_decrease_%': 'Increase/Decrease by %',
        'increase_decrease_amount': 'Increase/Decrease by Amount',
        'abs': 'ABS',
        'modify_values': 'Modify Values'
    };
    private show_popup:boolean = false; // show or hide popup
    private current_absolute_value:number;
    private current_absolute_value_formated:string;
    private current_percent_value:number = 0;
    private current_percent_value_formated:string;
    private reset_value: boolean = false; // if user press "Reset to Default" it will be true
    private type_popup:string;
    private leftPositon:string;
    private topPositon:string;
    private data:PopupData;
    private numeral = require('numeral');

    // Return cursor position after focus input
    _getCursorPosition(el) {
        const val = el.value;
        return val.slice(0, el.selectionStart).length;
    }

    // valid value after change percent if user change it manual
    validKeypress(event: any) {
        let cursor_position = this._getCursorPosition(event.target);
        let reg;
        if (this.current_percent_value_formated.length === 0 || (cursor_position === 0 && this.current_percent_value_formated.substring(0,1) !== '-')) {
            reg = /[0-9]|[-]/;
        } else {
            if (this.current_percent_value_formated.search(/[.]/i) === -1 && this.current_percent_value_formated!== '-') {
                reg = /[0-9]|[.]/;
            } else {
                reg = /[0-9]/;
            }
        }
        if (!event.key.match(reg)) {
            return false;
        }
    }

    // Get ABS format value
    getABSFormatValue() {
        this.current_absolute_value_formated = this.numeral(this.current_absolute_value).format(this.data.abs_format);
    }

    // Set ABS format value
    setABSFormatValue(value: string) {
        return this.numeral().set(value).value();
    }

    // Get Percent format value
    getPercentFormatValue() {
        this.current_percent_value_formated = this.numeral(this.current_percent_value).format(this.data.percent_format);
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['inputData']) {
            this.data = ch['inputData']['currentValue'];
            if (typeof this.data == "object" && this.data !== null) {

                // Update popup`s current values and show its
                if (this.inputData['type_popup'] !== undefined) {
                    this.current_absolute_value = this.inputData.value;
                    this.getABSFormatValue();

                    // type popup
                    this.type_popup = this.data.type_popup;

                    // get current percent value
                    this.current_percent_value = 0;
                    this.getPercentFormatValue();

                    // set current popup position
                    this.leftPositon = this.data.coordinate_x + 'px';
                    this.topPositon = this.data.coordinate_y - 117 + 'px';

                    // show popup
                    this.show_popup = true;
                }
            }
        }
    }

    onCansel() {
        this.show_popup = false;
        this.reset_value = false;
        this.current_percent_value = 0;
    }

    onReset() {
        // this.current_absolute_value = this.data.default_value;
        // this.reset_value = true;
        this.current_percent_value = 0;
        this.current_absolute_value = this.data.value;
        this.getPercentFormatValue();
        this.getABSFormatValue();
    }

    plusAbsoluteValue() {
        this.current_absolute_value = this.current_absolute_value + this.data.absolute_step;
        this.getABSFormatValue();
        this.changePercent();
    }

    minusAbsoluteValue() {
        this.current_absolute_value = this.current_absolute_value - this.data.absolute_step;
        this.getABSFormatValue();
        this.changePercent();
    }

    // change value if user press plus/minus percent
    changeAbsoluteValue() {
        if (this.reset_value) {
            this.current_absolute_value = this.data.default_value + this.data.default_value * this.current_percent_value;
        } else {
            this.current_absolute_value = this.data.value + this.data.value * this.current_percent_value;
        }
        this.getABSFormatValue();
    }

    // change value if user change it manual
    changeUserValue(event: any) {
        const value = event.target.value;
        let val = value.toString().trim();
        if (val.length !== 0 && !isNaN(val)) {
            this.current_absolute_value = this.setABSFormatValue(val);
        } else {
            if (this.reset_value) {
                this.current_absolute_value = this.data.default_value;
            } else {
                this.current_absolute_value = this.data.value;
            }
        }
        this.getABSFormatValue();
        this.changePercent();
    }

    // remove symbol from value input is user focused it
    clearUserValue(event: any) {
        const value = event.target.value;
        let val = value.replace(/[^.0-9^-]/g, '');
        this.current_absolute_value_formated = val;
    }

    // change percent if user change it manual
    changeUserPercent(value: string) {
        let val = value.trim();
        if (val.slice(-1) === '%') {
            val = val.slice(0, -1);
        }
        if (val.length > 0) {
            this.current_percent_value = this.setABSFormatValue(val) / 100;
        } else {
            this.current_percent_value = 0;
        }
        this.changeAbsoluteValue();
        this.getPercentFormatValue();
    }

    // remove symbol from percent input is user focused it
    clearUserPercent(value: string) {
        let val = value.trim();
        if (val.slice(-1) === '%') {
            val = val.slice(0, -1);
            this.current_percent_value_formated = val;
        }
    }

    plusPercentValue() {
        this.current_percent_value = this.current_percent_value + (this.data.percent_step) / 100;
        this.changeAbsoluteValue();
        this.getPercentFormatValue();
    }

    minusPercentValue() {
        this.current_percent_value = this.current_percent_value - (this.data.percent_step) / 100;
        this.changeAbsoluteValue();
        this.getPercentFormatValue();
    }

    // change persent if user press plus/minus value
    changePercent() {
        if (this.data.type_value === 'number') {
            if (this.data.value === 0) {
                this.current_percent_value = 0;
            } else {
                if (this.reset_value) {
                    this.current_percent_value = (this.current_absolute_value / this.data.default_value) - 1;
                } else {
                    this.current_percent_value = (this.current_absolute_value / this.data.value) - 1;
                }
            }
        } else {
            if (this.reset_value) {
                this.current_percent_value = (this.current_absolute_value - this.data.default_value) / 100;
            } else {
                this.current_percent_value = (this.current_absolute_value - this.data.value) / 100;
            }
        }
        this.getPercentFormatValue();
    }

    // return new value to parent component
    onApply(){
        this.popupRequest.emit(this.numeral(this.current_absolute_value).value());
        this.onCansel();
    }
}
