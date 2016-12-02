backup = {
  "var_names" : ["Sales", "Popularity" , "Income", "Costs"],
  "var_properties" :
                  [
                      {"var":"Sales","prop":"total","value":"1000"},
                      {"var":"Income","prop":"total","value":"1000"},
                      {"var":"Costs","prop":"total","value":"1000"}
                  ],
  "time_series" : [
                  {"var": "Sales", "ts": "annual", "line": [0,1,2,3,4,5]},
                  {"var": "Income", "ts": "annual", "line": [0,1,2,3,4,5]},
                  {"var": "Costs", "ts": "annual", "line": [0,1,2,3,4,5]}
                  ],
  "scalars" : [
                  {"var": "Loan", "ts": "annual", "value": 10},
                  {"var": "Tax", "ts": "annual", "value": 10},

              ],
  "periods_series":[
                  {"var": "Sales", "ts" : "annual", "period": ("2012","2013"), "value":0},
                  {"var": "Sales", "ts" : "annual", "period": ("2013","2014"), "value":1},
                  {"var": "Sales", "ts" : "annual", "period": ("2014","2015"), "value":2},
                  {"var": "Sales", "ts" : "annual", "period": ("2015","2016"), "value":3},
                  {"var": "Sales", "ts" : "annual", "period": ("2016","2017"), "value":4},
                  {"var": "Sales", "ts" : "annual", "period": ("2017","2018"), "value":5},
                  {"var": "Income", "ts" : "annual", "period": ("2012","2013"), "value":0},
                  {"var": "Income", "ts" : "annual", "period": ("2013","2014"), "value":1},
                  {"var": "Income", "ts" : "annual", "period": ("2014","2015"), "value":2},
                  {"var": "Income", "ts" : "annual", "period": ("2015","2016"), "value":3},
                  {"var": "Income", "ts" : "annual", "period": ("2016","2017"), "value":4},
                  {"var": "Income", "ts" : "annual", "period": ("2017","2018"), "value":5},
                  {"var": "Costs", "ts" : "annual", "period": ("2012","2013"), "value":0},
                  {"var": "Costs", "ts" : "annual", "period": ("2013","2014"), "value":1},
                  {"var": "Costs", "ts" : "annual", "period": ("2014","2015"), "value":2},
                  {"var": "Costs", "ts" : "annual", "period": ("2015","2016"), "value":3},
                  {"var": "Costs", "ts" : "annual", "period": ("2016","2017"), "value":4},
                  {"var": "Costs", "ts" : "annual", "period": ("2017","2018"), "value":5}
                  ]
}

