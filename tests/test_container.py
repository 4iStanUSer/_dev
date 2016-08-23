from iap.forecasting.workbench.container.container import Container

def test_container():
    c = Container()
    time_line_annual = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    time_line_quarterly = ['Q1_2016', 'Q2_2016', 'Q3_2016', 'Q4_2016',
                           'Q1_2017', 'Q2_2017', 'Q3_2017', 'Q4_2017',
                           'Q1_2018', 'Q2_2018', 'Q3_2018', 'Q4_2018'
                           ]
    c.add_time_scale('annual', time_line_annual)
    c.add_time_scale('quarterly', time_line_quarterly)

    japan = c.add_entity(['Japan'])
    chocolate = japan.add_child('Chocolate')
    print(chocolate.get_variables_names())
    units = chocolate.force_variable('Units')
    print(chocolate.get_variables_names())
    annual_ts_units = units.force_time_series('annual')
    annual_ts_units.set_values(2013, [4, 5, 6])
    print(annual_ts_units.get_values())
    print(annual_ts_units.get_values(2012, 4))
    units.name = 'Dollars'
    print(chocolate.get_variables_names())

    kk = 7