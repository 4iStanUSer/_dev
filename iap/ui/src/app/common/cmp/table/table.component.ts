import { Component, Input, OnChanges, Output, EventEmitter } from '@angular/core';


@Component({
  selector: 'table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css'],
})
export class TableComponent implements OnChanges {
  @Input() data: Array<Object>;
  @Input() options: Object;
  @Output() current_id: EventEmitter<number> = new EventEmitter<number>();

  current_data: Array<Object>;
  current_options: Object = {};
  current_filter: Object = {};

  ngOnChanges() {
    this.current_data = this.data;
    this.current_options = this.options;

    // Default Sort
    this.__sortByKey();

    // Init Current filter
    this.__initCurrentFilter();
  }

  // -----------------------------------  Sort list  ----------------------------------- //
  __sortByKey() {
    if (this.current_options['logs']) {
      console.log('---__sortByKey', this.current_options['default_sort']['field_name'], this.current_options['default_sort']['order']);
    }
    const field = this.current_options['default_sort']['field_name'];
    const order = this.current_options['default_sort']['order'];
    let sort_list = this.current_data;
    if (sort_list !== undefined && sort_list.length > 0) {
      return sort_list.sort(function (a, b) {
        let x = a[field];
        let y = b[field];

        if (typeof x == "string") {
          x = x.toLowerCase();
        }
        if (typeof y == "string") {
          y = y.toLowerCase();
        }
        if (order === true) {
          return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        } else {
          return ((x > y) ? -1 : ((x < y) ? 1 : 0));
        }
      });
    }
  }

  onToggleSort(field: string) {
    let header_rows = this.current_options['header_rows'].filter((item: Object) => item['name'] === field);
    if (header_rows.length > 0 && header_rows[0]['sort'] === true) {
      if (this.current_options['logs']) {
        console.log('---onToggleSort', field, !this.current_options['default_sort']['order']);
      }
      this.current_options['default_sort']['field_name'] = field;
      this.current_options['default_sort']['order'] = !this.current_options['default_sort']['order'];

      // Run new sorting
      this.__sortByKey();
    }
  }

  // -----------------------------------  Filter list  ----------------------------------- //
  __initCurrentFilter(){
    let header_filter_rows = this.current_options['header_rows'].filter((item: Object) => item['filter'] === true);
    if (header_filter_rows.length > 0) {
      for (let item of header_filter_rows) {
        if (this.current_options['logs']) {
          console.log('---__initCurrentFilter', item);
        }
        this.current_filter[item.name] = '';
      }
    }
  }

  __maskFilter(item: Object, mask: Object){
    let status = true;
    if (mask !== undefined) {
      let filterSelectKeys = Object.keys(mask);
      for (let k of filterSelectKeys) {
        if (item[k].toLowerCase().search(mask[k]) === -1 && mask[k]) {
          status = false;
        }
      }
    }
    return status;
  }

  __runFilter() {
    if (this.current_options['logs']) {
      console.log('--------------------__runFilter', this.current_filter);
    }
    if (this.data.length > 0) {
      this.current_data = [];
      for (let scenario of this.data) {
        if (this.__maskFilter(scenario, this.current_filter)) {
          this.current_data.push(scenario);
        }
      }
    }
  }

  onFilter(event: any) {
    this.current_filter[event.target.name] = event.target.value;
    this.__runFilter();
    if (this.current_options['logs']) {
      console.log('---onFilter', event.target.value, event.target.name, this.current_filter);
    }
    // New Sort
    this.__sortByKey();
  }

  // ----------------------------------  Select action  ---------------------------------- //
  onSelect(event: any) {
    let current_element = event.currentTarget;
    this.__clearSelect();

    current_element.classList.add("active");
    const cur_id = parseInt(current_element.attributes['data-id'].value);
    this.current_id.emit(cur_id);
    if (this.current_options['logs']) {
      console.log('---onSelect emit', cur_id, this.current_id);
    }
  }

  __clearSelect():void {
      let elements: any = document.getElementsByClassName('table-body-row');
      for (let element of elements) {
          element.classList.remove("active");
      }
  }

  clearSelect():void {
      this.__clearSelect();
      this.onUpdateData();
  }

  // ----------------------------------  Update action  ---------------------------------- //
  onUpdateData() {
    if (this.current_options['logs']) {
      console.log('---onUpdateData');
    }
    this.current_data = this.data;

    // Update filter
    this.__runFilter();

    // Update Sort
    this.__sortByKey();
  }
}
