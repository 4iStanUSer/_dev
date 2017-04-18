import { Injectable } from '@angular/core';
import { AjaxService } from "../../common/service/ajax.service";





@Injectable()
export class DataService {

    timelabel_hierarchy:any=null;
    values:any = null;

    constructor(private http:AjaxService){}

  getData(){
    return [
      {id: 1, title: "yasd1", name:"asdasd1"},
      {id: 2, title: "asd2", name:"asdasd2"},
      {id: 3, title: "asd3", name:"asdasd3"},
      {id: 4, title: "asd3", name:"asdasd3"},
      {id: 5, title: "wasd4", name:"asdasd4"},
      {id: 6, title: "asd5", name:"asdasd5"},
      {id: 7, title: "rel6", name:"rel5rel 6"}
    ];
  }
  getSimulatorData(){
    console.log("Simulator Custom Data");

    this.http.post(
        {
            url_id: '/forecast/get_custom_data',
            sync: true,
            data: {}
        }).subscribe
        (
          (d)=> {
              console.log(d);
          }
        );

     console.log("Simulator Page Data");

    this.http.post({
            url_id: '/forecast/get_simulator_page_data',
            sync: true,
            data: {}
        }).subscribe(
        (d)=>{
            console.log(d['data']);

            this.timelabel_hierarchy = d['hierarchy']['timelable_tree'];
            this.values = d['data']['values'];
            this.get_table_data();
        }

    )


  }
  get_table_data(){
      console.log("Get Table Data", this.timelabel_hierarchy);
      let time_table=[];

      for(var time_stamp = 0; time_stamp < this.timelabel_hierarchy.length; time_stamp++){

          let time_scale = this.timelabel_hierarchy[time_stamp]['timescale'];


          time_table[time_stamp] = {};
          time_table[time_stamp]['timelable_id'] =
              this.timelabel_hierarchy[time_stamp]['id'];
          time_table[time_stamp]['parent_index'] =
              this.timelabel_hierarchy[time_stamp]['parent_index'];
          time_table[time_stamp]['values'] = [];
          for (var _variable in this.values['custom'][time_scale]){

            let c_variable =  this.values['custom'][time_scale][_variable];
            let d_variable =  this.values['default'][time_scale][_variable];
            try {
                let c_cell = {};
                c_cell['stamp'] = c_variable['stamps'][time_stamp];
                c_cell['var_name'] = _variable;
                c_cell['type'] = "custom";
                c_cell['value'] = c_variable['values'][time_stamp];;
                c_cell['cagr'] = c_variable['cagrs'][time_stamp];
                c_cell['abs_growth'] = c_variable['abs_growth'][time_stamp];
                c_cell['relative_growth'] = c_variable['relative_growth'][time_stamp];
                time_table[time_stamp]['values'].push(c_cell);

                let d_cell = {};
                d_cell['stamp'] = d_variable['stamps'][time_stamp];
                d_cell['var_name'] = d_variable;
                d_cell['type'] = "default";
                d_cell['value'] = d_variable['values'][time_stamp];;
                d_cell['cagr'] = d_variable['cagrs'][time_stamp];
                d_cell['abs_growth'] = d_variable['abs_growth'][time_stamp];
                d_cell['relative_growth'] = d_variable['relative_growth'][time_stamp];
                time_table[time_stamp]['values'].push(d_cell);
                }
            catch (e){
                console.log(e);

            }
          }
      }
      return time_table;
  }



}

/*
getAccordionData(){
    return [
      {
        header_background_color: '#fff',
        top_values: [
          {
            name: 'inflation',
            width: '150px',
            background_color: '#cfd5de',
            values: [
              {id: 111, value: 'Inflation', parent_id: 0, background_color: '#fff', format:''},
              {id: 222, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3331, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3332, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3333, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3334, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3335, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3336, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3337, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3338, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 3339, value: '--inflation', parent_id: 111, background_color: '#fff', format:''},
              {id: 444, value: 'Inflation', parent_id: 0, background_color: '#ff0000', format:''},
              {id: 5551, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5552, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5553, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5554, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5555, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5556, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5557, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5558, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 5559, value: '--inflation', parent_id: 444, background_color: '#fff', format:''},
              {id: 666, value: '--inflation', parent_id: 444, background_color: '#fff', format:''}
            ]
          }
        ]
      },
      {
        header_background_color: '#fff',
        top_values: [
          {
            name: 'metric',
            label: 'Metric',
            width: '150px',
            background_color_label: '#cfd5de',
            background_color_body: '#cfd5de',
            values: [
              {id: 111, value: 'Metric', parent_id: 0, background_color: '#fff', format:''},
              {id: 222, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3331, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3332, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3333, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3334, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3335, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3336, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3337, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3338, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 3339, value: '--metric', parent_id: 111, background_color: '#fff', format:''},
              {id: 444, value: 'Metric', parent_id: 0, background_color: '#ff0000', format:''},
              {id: 5551, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5552, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5553, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5554, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5555, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5556, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5557, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5558, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 5559, value: '--metric', parent_id: 444, background_color: '#fff', format:''},
              {id: 666, value: '--metric', parent_id: 444, background_color: '#fff', format:''}
            ]
          }
        ]
      },
      {
        header_name: 'history',
        header_label: 'History',
        header_background_color: '#cfd5de',
        top_values: [
          {
            name: '2010-01-01T05:06:07',
            format: "YYYY",
            type_value: 'date',
            label: '2010-01-01T05:06:07',
            width: '90px',
            background_color_label: '#cfd5de',
            background_color_body: '#9b9da0',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00', action: true},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00', action: true},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00', action: true},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00', action: true},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00', action: true},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00', action: true},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00', action: true},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00', action: true},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00', action: true},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00', action: true},
            ],
          },
          {
            name: 'row_2',
            label: 'Row 2',
            width: '90px',
            background_color_label: '#cfd5de',
            background_color_body: '#9b9da0',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          }
        ],
        sub_values: [
          {
            parent_name: '2010-01-01T05:06:07',
            show_key: 'k1',
            format: "YYYY MM",
            name: '2010-01-01T05:06:07',
            type_value: 'date',
            label: '2010-01-01T05:06:07',
            width: '120px',
            background_color_label: '#9b9da0',
            background_color_body: '#fff',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          },
          {
            parent_name: '2010-01-01T05:06:07',
            show_key: 'k1',
            format: "YYYY MM",
            name: '2010-02-01T05:06:07',
            type_value: 'date',
            label: '2010-02-01T05:06:07',
            width: '120px',
            background_color_label: '#9b9da0',
            background_color_body: '#fff',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          },
          {
            parent_name: '20111031',
            show_key: 'k2',
            name: 'sub_row_11',
            label: 'K2 Sub Row 11',
            width: '120px',
            background_color_label: '#9b9da0',
            background_color_body: '#fff',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          },
          {
            parent_name: 'row_2',
            show_key: 'k1',
            name: 'sub_row_2',
            label: 'K1 Sub Row 2',
            width: '120px',
            background_color_label: '#9b9da0',
            background_color_body: '#fff',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          }
        ],
      },
      {
        header_name: 'forecast',
        header_label: 'Forecast',
        header_background_color: '#f9ddb8',
        top_values: [
          {
            name: 'row_3',
            label: 'Row 3',
            width: '90px',
            background_color_label: '#ff0000',
            background_color_body: '#fff7ed',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'0,0.00', action: true},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          },
          {
            name: 'row_4',
            label: 'Row 4',
            width: '90px',
            background_color_label: '#cfd5de',
            background_color_body: '#fff7ed',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          }
        ],
        sub_values: [
          {
            parent_name: 'row_3',
            show_key: 'k1',
            name: 'sub_row_3',
            label: 'K1 Sub Row 3',
            width: '120px',
            background_color_label: '#cfd5de',
            background_color_body: '#9b9da0',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00', action: true},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          },
          {
            parent_name: 'row_4',
            show_key: 'k2',
            name: 'sub_row_4',
            label: 'K2 Sub Row 4',
            width: '120px',
            background_color_label: '#cfd5de',
            background_color_body: '#9b9da0',
            values: [
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 6, value: 16, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 1, value: 11, parent_id: 0, background_color: '#0100ff', format:'$0,0.00'},
              {id: 2, value: 12, parent_id: 1, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 3, value: 13, parent_id: 1, background_color: '#ff0000', format:'$0,0.00'},
              {id: 4, value: 14, parent_id: 0, background_color: '#cfd5de', format:'$0,0.00'},
              {id: 5, value: 15, parent_id: 4, background_color: '#cfd5de', format:'$0,0.00'},
            ],
          }
        ],
      }
    ];
}
*/
