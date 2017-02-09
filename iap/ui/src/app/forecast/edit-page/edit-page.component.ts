import { Component, OnInit } from '@angular/core';
import {element} from "protractor";
import {Element} from "@angular/compiler/src/ml_parser/ast";

const data: number[] = [11.2,22.54,24.0,12.2,14.5,0,100, 2];

@Component({
    selector: 'app-edit-page',
    templateUrl: 'edit-page.component.html',
    styleUrls: ['edit-page.component.css']
})

export class EditPageComponent{
  numbers = data;
  absolute_step = 1;
  percent_step = 1;
  type_value = 'number'; // 'number', 'rate'
  abs_format = '$0,0.[00]';
  percent_format = '0.[00]%';
  type_popup = 'extended'; // 'normal', 'extended')
  default_value = 50.66666;
  curent_data: any;

  showPopup(event: EventTarget): void {
      let curent_element = event.target.innerHTML;

      if (!isNaN(curent_element)) {
          const coordinate_x = event.target.offsetLeft + event.target.offsetWidth / 2;
          const coordinate_y = event.target.offsetTop + event.target.offsetHeight / 2;
          const curent_value = parseFloat(curent_element);

          this.curent_data = {
              coordinate_x: coordinate_x,
              coordinate_y: coordinate_y,
              value: curent_value,
              type_value: this.type_value,
              abs_format: this.abs_format,
              percent_format: this.percent_format,
              type_popup: this.type_popup,
              absolute_step: this.absolute_step,
              percent_step: this.percent_step,
              default_value: this.default_value
          };
      }
  }

  popupRequest(event: EventTarget): void {
      console.log(event);
  }
}
