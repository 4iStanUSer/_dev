import pytest
import json
from iap.forecasting.workbench.container.timelines import TimeLineManager
from iap.forecasting.workbench.container.entity_data import *

@pytest.fixture
def backup():
    from conf_test import backup
    return backup

@pytest.fixture
def data():
    """Load test data

    :return:

    """

    with open('json/timeline_manager/timeline_manager.json') as data_file:
        time_line = json.load(data_file)
    return time_line


@pytest.fixture
def time_line_manager(data):
    """Fixture that prepare timeline manager

    :param data:
    :return:

    """
    ts_properties = data['properties']
    alias = data['alias']
    top_ts_points = data['top_ts_points']

    _time_line_manager = TimeLineManager()
    _time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
    return _time_line_manager

@pytest.fixture
def entity_data(time_line_manager):
    """Entity data

    :param time_line_manager:
    :return:

    """
    _entity_data = EntityData(time_line_manager)
    return _entity_data


def test_get_backup(entity_data, backup):
    """Test for get_backup method

    :param entity_data:
    :param backup:
    :return:

    """

    entity_data.load_backup(backup)
    expected = backup
    actual = entity_data.get_backup()
    assert actual.keys() == expected.keys()
    assert sorted(actual['var_names']) == sorted(expected['var_names'])
    assert sorted(actual['periods_series'], key = lambda series: series['var']) == \
           sorted(actual['periods_series'], key = lambda series: series['var'])
    assert sorted(actual['var_properties'], key=lambda series: series['var']) == \
           sorted(actual['var_properties'], key=lambda series: series['var'])
    assert sorted(actual['var_names']) == sorted(expected['var_names'])
    assert sorted(actual['time_series'], key=lambda series: series['var']) == \
           sorted(actual['time_series'], key=lambda series: series['var'])
    assert sorted(actual['scalars'], key=lambda series: series['value']) == \
           sorted(actual['scalars'], key=lambda series: series['value'])


def test_get_ts_vals(entity_data, backup):
    '''

    Args:
        (string): var_name - name of variable
        (string):ts_name - timeseries name
        (tuple): period in timeseries
        (int): length of time series
    Return:
        (list): slice of time series by specific period

    :return:

    '''

    entity_data.load_backup(backup)
    expected = [0,1]
    actual = entity_data.get_ts_vals("Sales", "annual", ("2012", "2013"), 0)
    assert expected == actual
    # Failed test

    entity_data.load_backup(backup)
    expected = [4, 5]
    actual = entity_data.get_ts_vals("Costs", "annual", ("2016", "2017"), 4)
    assert expected == actual

    expected = [0, 1, 2, 3, 4, 5]
    actual = entity_data.get_ts_vals("Income", "annual", ("2012", "2017"), 3)
    assert expected == actual

    entity_data.load_backup(backup)
    expected = [0, 1, 2, 3, 4]
    actual = entity_data.get_ts_vals("Sales", "annual", ("2012",None), 4)

    assert expected == actual


def test_set_ts_vals(entity_data, backup):
    """
    Args:
        (string): var_name - variable name
         (string): ts_name - timeseries name
        (list): values -list of values
        (None): stamp - initial points
    Return:

    :return:

    """

    entity_data.load_backup(backup)
    entity_data.set_ts_vals("Sales", "annual", [1, 2], "2012")
    expected = [1, 2, 2, 3, 4, 5, 0]
    actual = entity_data._time_series[('Sales', 'annual')]
    assert actual == expected
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_ts_vals("Income", "annual", [0, 1], "2014")
    expected = [0, 1, 0, 1, 4, 5, 0]
    actual = entity_data._time_series[('Income', 'annual')]
    assert actual == expected
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_ts_vals("Costs", "annual", [1], "2016")
    expected = [0, 1, 2, 3, 1, 5, 0]
    actual = entity_data._time_series[('Costs', 'annual')]
    assert actual == expected


def test_get_period_vals(entity_data, backup):
    """Test for get_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    """

    entity_data.load_backup(backup)
    expected = 0
    actual = entity_data.get_period_val("Sales", "annual", ("2012", "2013"))
    assert expected == actual

    expected = 4
    actual = entity_data.get_period_val("Sales", "annual", ("2016", "2017"))
    assert expected == actual

    expected = 1
    actual = entity_data.get_period_val("Sales", "annual", ("2013", "2014"))
    assert expected == actual

    expected = 0
    actual = entity_data.get_period_val("Costs", "annual", ("2012", "2013"))
    assert expected == actual

    expected = 2
    actual = entity_data.get_period_val("Costs", "annual", ("2014", "2015"))
    assert expected == actual

    expected = 5
    actual = entity_data.get_period_val("Costs", "annual", ("2017", "2018"))
    assert expected == actual


def test_set_period_vals(entity_data, backup):
    """Test for set_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    """

    entity_data.load_backup(backup)
    expected = 10
    entity_data.set_period_val("Sales", "annual", ("2012", "2013"), 10)
    actual = entity_data._periods_series[("Sales", "annual")][("2012", "2013")]
    assert actual == expected


def test_get_all_period(entity_data, backup):
    """Test for method get all periods

    Args:
        (string): var_name - variable name
        (string): ts_name  - time series name

    Return:
        (list): of periods

    :param entity_data:
    :param backup:
    :return:

    """

    entity_data.load_backup(backup)

    expected = [('2012', '2013'), ('2013', '2014'), ('2014', '2015'), ('2015', '2016'), ('2016', '2017'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Sales", "annual")
    print(list(actual))
    print(list(expected))
    assert sorted(list(expected), key=lambda l: l[0]) == \
           sorted(list(actual), key=lambda l: l[0])

    expected = [('2012', '2013'), ('2013', '2014'), ('2014', '2015'),('2015', '2016'), ('2016', '2017'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Costs", "annual")
    assert sorted(list(expected), key=lambda l: l[0]) == \
           sorted(list(actual), key=lambda l: l[0])

    expected = [('2012', '2013'), ('2013', '2014'), ('2014', '2015'), ('2015', '2016'), ('2016', '2017'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Income", "annual")
    assert sorted(list(expected), key=lambda l: l[0]) ==\
           sorted(list(actual), key=lambda l: l[0])


def test_is_exist(entity_data, backup):
    """Bool function check wether variable are in backup

    Args:
        (string): var_name - name of variable
        (string): ts_name - timeseries name
        (DataType): data_type - specific data type

    Return:
        (bool)

    :return:

    """

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Sales", "annual", SlotType.time_series)
    assert expected == actual
    # Failed test

    expected = True
    actual = entity_data.is_exist("Tax", "annual", SlotType.scalar)
    assert expected == actual

    expected = False
    actual = entity_data.is_exist("Cloth", "annual", SlotType.time_series)
    assert expected == actual

    expected = True
    actual = entity_data.is_exist("Loan", "annual", SlotType.scalar)
    assert expected == actual

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Income", "annual", SlotType.period_series)
    assert expected == actual


def test_rename_variable(entity_data, backup):
    """Method that rename variable

    Args:
        (string): old_name - old name of variable
        (string): new_name - new name of variable

    Return:

    :param :
    :param :
    :return:

    """

    entity_data.load_backup(backup)
    entity_data.rename_variable("Sales", "Pre-sales")
    assert "Pre-sales" in list(entity_data._variables.keys())
    assert "Sales" not in list(entity_data._variables.keys())

    entity_data.load_backup(backup)
    entity_data.rename_variable("Costs", "Pre-sales")
    assert "Pre-sales" in list(entity_data._variables.keys())
    assert "Costs" not in list(entity_data._variables.keys())

    entity_data.load_backup(backup)
    entity_data.rename_variable("Income", "Pre-sales")
    assert "Pre-sales" in list(entity_data._variables.keys())
    assert "Income" not in list(entity_data._variables.keys())


def test_set_var_property(entity_data, backup):
    '''Set specific value for variable propery
    Args:
        (string): var_name -variable name
        (string): prop_name - property name
        (obj): value

    Return:

    :return:

    '''

    entity_data.load_backup(backup)
    entity_data.set_var_property("Sales", 'total', 10)
    assert entity_data._variables['Sales'] == {'total': 10}


    entity_data.load_backup(backup)
    entity_data.set_var_property("Costs", 'total', 100)
    assert entity_data._variables["Costs"] == {'total': 100}
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Income", 'total', 500)
    assert entity_data._variables["Income"] == {"total": 500}


def test_get_var_property(entity_data, backup):
    """Return value of variable property
    Args:
        (string): var_name - variable name
        (string): prop_name -  property name
    Return:
        value
    :return:

    """

    entity_data.load_backup(backup)
    expected = "1000"
    actual = entity_data.get_var_property("Sales", "total")
    assert actual == expected

    expected = "1000"
    actual = entity_data.get_var_property("Costs", "total")
    assert actual == expected

    expected = "1000"
    actual = entity_data.get_var_property("Income", "total")
    assert actual == expected


def test_get_var_properties(entity_data, backup):
    """Return all properties of specific variable
    Args:
        (string): var_name - variable name
    Return:
        value
    """

    entity_data.load_backup(backup)
    expected = {"total":"1000"}
    actual = entity_data.get_var_properties("Sales")
    assert actual == expected

    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Income")
    assert actual == expected

    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Costs")
    assert actual == expected


def test_var_names(entity_data, backup):
    """Return value of variable property

    Args:
        (string): var_name - variable name
        (string): prop_name -  property name
    Return:
        value
    """

    entity_data.load_backup(backup)
    actual = entity_data.var_names
    expected = ['Sales','Popularity', 'Income', 'Costs']

    assert sorted(list(expected)) == sorted(list(actual))


def test_add_variable(entity_data, backup):
    """Add new variable to backup

    Args:
        (string): var_name
    Return:

    :return:

    """

    entity_data.load_backup(backup)
    entity_data.add_variable("New Sales")
    actual = entity_data._variables.keys()

    assert "New Sales" in actual
    assert list(actual).count("New Sales") == 1

    entity_data.load_backup(backup)
    entity_data.add_variable("Sales")
    actual = entity_data._variables.keys()

    assert "Sales" in actual
    assert list(actual).count("Sales") == 1

    entity_data.load_backup(backup)
    entity_data.add_variable(5)
    actual = entity_data._variables.keys()

    assert 5 in actual
    assert list(actual).count(5) == 1


def test_get_scalar_val(entity_data, backup):
    """Test for method get scalar:
    Check excepted and output value equality

    Args:
        (string): var_name - variable name
        (string): ts_name - name of time series
    Return:
        list()

    :param entity_data:
    :param backup:
    :return:

    """
    entity_data.load_backup(backup)

    expected = 10
    actual = entity_data.get_scalar_val('Loan', 'annual')
    assert expected == actual

    expected = 10
    actual = entity_data.get_scalar_val('Tax', 'annual')
    assert expected == actual

    expected = 100
    actual = entity_data.get_scalar_val('Rate', 'annual')
    assert expected == actual

    expected = 0
    actual = entity_data.get_scalar_val('Index', 'annual')
    assert expected == actual


def test_set_scalar_val(entity_data, backup):
    """Return list of variables

    Args:
        (string): var_name
        (string): ts_name
        (int): value

    :return:

    """
    entity_data.load_backup(backup)

    entity_data.set_scalar_val('Loan', 'annual', 500)
    expected = 500
    actual =  entity_data._scalars[('Loan', 'annual')]
    assert expected == actual

    entity_data.set_scalar_val('Tax', 'annual', 1000)
    expected = 1000
    actual = entity_data._scalars[('Tax', 'annual')]
    assert expected == actual

    entity_data.set_scalar_val('Rate', 'annual', 2000)
    expected = 2000
    actual = entity_data._scalars[('Rate', 'annual')]
    assert expected == actual

    entity_data.set_scalar_val('Index', 'annual', 4000)
    expected = 4000
    actual = entity_data._scalars[('Index', 'annual')]
    assert expected == actual
