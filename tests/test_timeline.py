import pytest
import json

from iap.forecasting.workbench.container.timelines import TimeLineManager


@pytest.fixture
def load_data():
    with open('json/timeline.json') as data_file:
        time_line = json.load(data_file)
    return time_line


def setup():
    pass

def teardrop():
    pass

def test_time_line_manager():

    '''

    Testing timeline manager initialisation

    :return:

    '''

    pass

def test_get_back_up(load_data):

    '''

    Testing get_backup(self) method

    :return:

    '''

    def get_load_backup(backup):

        time_line_manager = TimeLineManager()
        time_line_manager.load_backup(backup)
        print(time_line_manager.get_backup())
        return time_line_manager.get_backup()==backup

    assert get_load_backup(load_data) == True

    assert get_load_backup(load_data) == False


def test_load_timelines(load_data):

    '''

            :param ts_properties:

            {
                "annual": {"name": "Annual", "growth_lag": 1}

            }

            :param alias:

            {
                "all": {"annual": ("2013", "2018")},
                "history": {"annual": ("2013", "2015")},
                "forecast": {"annual": ("2016", "2018")}
            }

            :param top_ts_points:

            [....]

            :return:

            Process dictionary and add necessary data to object attributes

            self.timescales = {}

            [{'timeline': [{'children': [], 'name_short': '2012', 'name_full': '2012', 'depth': 0},
                           {'children': [], 'name_short': '2013', 'name_full': '2013', 'depth': 0},
                           {'children': [], 'name_short': '2014', 'name_full': '2014', 'depth': 0},
                           {'children': [], 'name_short': '2015', 'name_full': '2015', 'depth': 0},
                           {'children': [], 'name_short': '2016', 'name_full': '2016', 'depth': 0},
                          {'children': [], 'name_short': '2017', 'name_full': '2017', 'depth': 0},
                          {'children': [], 'name_short': '2018', 'name_full': '2018', 'depth': 0}],
                          'growth_lag': 1, 'name': 'annual'}]


            self._period_alias:
                        {'forecast':
                        {'annual': ['2016', '2018']}, 'all': {'annual': ['2013', '2018']}, 'history': {'annual': ['2013', '2015']}}


    '''

    def load_timeline(load_data):

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties,alias,top_ts_points)

        return time_line_manager

    #check ._timesclales equality

    #check ._period_alias equality

    print(load_timeline(load_data)._timescales)

    assert load_timeline(load_data)._period_alias == load_data['alias']

    #assert load_timeline(load_unknow_data)._timescales


def test_process_inp_node():

    '''
    Test for process_inp_node

    :return:

    '''
    pass

    #check timescale equaliy

def test_get_ts(load_data):

    '''

    Testing get_ts(self,name) - function for testing get_ts
                                return dictionary information about time series by name
    ---

    Input: name of time series

    Output: dictionary inforamtion about time series

    :param name:
    :return:


    '''

    #test will check input and output equality

    def get_ts(name):
        #TimeLineManager Preparation

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return  time_line_manager._get_ts(name)

    print(get_ts('annual'))

    print(get_ts('2013'))

    #provide some verification

def test_get_growth_lag(load_data):

    '''

    Test for get_growth_lag

    :param self:
    :param ts_name:
    :return:

    '''

    def get_growth_lag(ts_name):

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_growth_lag(ts_name)

    print(get_growth_lag('annuals'))


def test_get_timeline_tree():
    pass

def test__add_point_to_tree():
    pass

def test_get_name():
    pass

def get_time_length():
    pass

def test_get_index():
    pass

def test_get_label():
    pass

def get_period_by_aliase():
    pass

def get_timeline_by_alise():
    pass

def test_get_last_actual():
    pass

def test_get_growth_period():
    pass