import json

with open('json/timeline_manager/timeline_manager.json') as f:
    timeline = json.load(f)

with open('json/timeline_manager/timescale.timeline_correct.json') as f:
    timeline_correct = json.load(f)


def prep_timeseries_backup(timeline, timeline_correct):
    # load data
    ts_properties = timeline['properties']
    alias = timeline['alias']
    top_ts_points = timeline['top_ts_points']
    backup = {}
    backup['alias'] = {}
    backup['timescales'] = []

    for period_name, ts_borders in alias.items():
        backup['alias'][period_name] = ts_properties

    for props in ts_properties:
        for timeserie in timeline_correct:
            if props['name'] == timeserie['name']:
                time_line = timeserie['timeline']
                growth_lag = timeserie['growth_lag']
                backup['timescales'].append(dict(name=props['name'], growth_lag=growth_lag, timeline=time_line))
    return backup

#Entity Data Back_Up

backup = {
  "var_names" : ["Sales", "Popularity", "Income", "Costs"],
  "var_properties" :
                  [
                      {"var":"Sales","prop":"total","value": "1000"},
                      {"var":"Income","prop":"total","value": "1000"},
                      {"var":"Costs","prop":"total","value": "1000"}
                  ],
  "time_series" : [
                  {"var": "Sales", "ts": "annual", "line": [0, 1, 2, 3, 4, 5]},
                  {"var": "Income", "ts": "annual", "line": [0, 1, 2, 3, 4, 5]},
                  {"var": "Costs", "ts": "annual", "line": [0, 1, 2, 3, 4, 5]}
                  ],
  "scalars" : [
                  {"var": "Loan", "ts": "annual", "value": 10},
                  {"var": "Tax", "ts": "annual", "value": 10},
                  {"var": "Rate", "ts": "annual", "value": 100},
                  {"var": "Index", "ts": "annual", "value": 0},
                  {"var": "Sales", "ts": "annual", "value": 0}

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

#Interface Backup
interface_backup = {"container":
        [

        {
            "path": ["Ukraine"],
            "metas": ["Geo", "Country"],
            "data": backup,
            "insights": ["a", "b", "c", "d"]
        },
        {
            "path": ["Ukraine", "Odessa"],
            "metas": [["Geo", "Country"], ["Geo", "Region"]],
            "data": backup,
            "insights": []
        },
        {
            "path": ["Ukraine", "Kiev"],
            "metas": [["Geo", "Country"],["Geo", "Region"]],
            "data": backup,
            "insights": []
        },
        {
            "path": ["Ukraine", "Kiev", "Candy"],
            "metas": [["Geo", "Country"], ["Geo", "Region"], ["Food", "Delicios"]],
            "data": backup,
            "insights": []
        }
    ],
    "timeline": prep_timeseries_backup(timeline, timeline_correct)
}


#Tree
tree =[
  [
  {"timescale": "annual", "short_name": "2012", "parent_index": None, "full_name": "2012"},
  {"timescale": "month", "short_name": "Jan", "parent_index": 0, "full_name": "January"},
  {"timescale": "month", "short_name": "Feb", "parent_index": 0, "full_name": "February"},
  {"timescale": "month", "short_name": "Mar", "parent_index": 0, "full_name": "March"},
  {"timescale": "annual", "short_name": "2013", "parent_index": None, "full_name": "2013"},
  {"timescale": "month", "short_name": "Jan", "parent_index": 4, "full_name": "January"},
  {"timescale": "month", "short_name": "Feb", "parent_index": 4, "full_name": "February"},
  {"timescale": "month", "short_name": "Mar", "parent_index": 4, "full_name": "March"}
  ],
  {"annual": ["2012", "2013"], "month": ["January", "March"]}
]


