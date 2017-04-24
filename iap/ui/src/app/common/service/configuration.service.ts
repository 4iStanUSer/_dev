import { Injectable } from '@angular/core';
import { Http } from "@angular/http";

@Injectable()
export class ConfigurationService {
    /***
     *Configuration Servide
     * wraped Local Storage in order to store all configuration
     *
     * Have functionality for returning config for page, component
     * By given page name, component_name.
     *
     *
     * Also provided mechanism for updating existing component config
     *
     */
    private config:any;
    private symbol = "-*-";
  constructor(private http:Http){}
  _get_config()
  {
      /**
       * Get configuration from backend, and store it in Local Storage
       * in key - value schema.
       * Where key is string 'page_name-*-component_name-*-property'
       * Value is also string.
        */
    this.http.post('/get_config',"").subscribe
        (
          (d)=>
            {
              this.config = d.json();
              console.log(this.config);
              for (var page_name  in this.config)
              {
                  for (var comp_name in this.config[page_name])
                  {
                      for (var key in this.config[page_name][comp_name])
                      {
                          let _key  = page_name+this.symbol+comp_name + this.symbol + key;
                          let _val = this.config[page_name][comp_name][key];
                          localStorage.setItem(_key, _val);
                      }
                  }
              }
            }
        )
  }

  update_config(page_name:string,component_name:string, config:any)
  {
      /**
       * Update input config of mentioned page name or page name and component name
       * Return new created updated config
       *
       * @type {{}}
       * @private
       */
    let _configuration = {};

    for (var key in config){
            try {
                if (localStorage.getItem(page_name + this.symbol + component_name + this.symbol + key) != config[key]) {
                    _configuration[key] = localStorage.getItem(page_name + this.symbol + component_name + this.symbol + key)
                }
            }
            catch (e){
                try{
                    var index=0;
                    _configuration[page_name] = {};
                    for(index; index<localStorage.length; index+=1){
                        var _keys = localStorage.key(index).split(this.symbol);
                        if (page_name in _keys){
                            _configuration[page_name][_keys[1]]  = {}
                            _configuration[page_name][_keys[1]][_keys[2]] =
                                localStorage.getItem(localStorage.key(index));

                        }
                    }
                }
                catch (e){

                }
            }
    }
    console.log(_configuration);
    return _configuration;
    }



  get_configuration(page_name="None", component_name="None", key="None")
  {
      /**
       * Return value of configuration parameter by given page name and component name
       * If component name is not passed function will return configuration for whole page
       * by given page_name.
       * If none of parameter passed function return empty config.
        * @type {{}}
       * @private
       */
       let _configuration={};

       try{
            return localStorage.getItem(page_name+this.symbol+component_name+this.symbol+key);

        }
        catch (e){
            if (page_name!='None' && component_name!='None'){
                var index = 0;
                for(index; index<localStorage.length; index+=1){

                    var _keys = localStorage.key(index).split(this.symbol);

                    if (page_name && component_name in _keys){

                        _configuration[page_name] = {};
                        _configuration[page_name][component_name] =
                            localStorage.getItem(localStorage.key(index));

                    }

                }

                return _configuration;
            }
            else if(page_name!='None'){
                var index=0;
                for(index; index<localStorage.length; index+=1){
                    var _keys = localStorage.key(index).split(this.symbol);
                    if (page_name in _keys){
                        _configuration[page_name] = localStorage.getItem(localStorage.key(index));

                    }
                }
            }

            else {
                return _configuration;
            }
        }
  }


}

