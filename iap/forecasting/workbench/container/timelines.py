import copy
from iap.common.exceptions import *

class TimeLineManager:

    def __init__(self):
        ''' Initialisation of TimeLineManager

        '''

        self._timescales = []
        self._period_alias = dict()

    def get_backup(self):
        '''Return  attributes timesclales and period_alias in dictionary form

        list of dictionary with  keys name,growth_lag and timeline = [] - list 0f points
        self.timescales = [dict(name=name, growth_lag=props['growth_lag'], timeline=[])

        :return:

        '''

        return dict(timescales=self._timescales, alias=self._period_alias)

    def load_backup(self, backup):

        '''

        :param backup:

        :return:

        '''

        self._timescales =  backup['timescales']
        self._period_alias = backup['alias']

    def load_timelines(self, ts_properties, alias, top_ts_points):
        '''Process dictionary and add necessary data to object attributes:
        Args:
            (string): time series name
        Return:
            (list): time series content
        :param ts_properties: tamescale properties
                list of dictionary with key's - name,growth_lag
        :param alias:
                lsit of dictionary with key's - period_name, values - period for timeseries
        :param top_ts_points:

        :return:

        self.timescales:

        self.period_name:

        self._proceess_inp_node:

        '''

        for props in ts_properties:
            self._timescales.append(dict(name= props['name'], growth_lag=props['growth_lag'], timeline=[]))

        for period_name, ts_borders in alias.items():
            self._period_alias[period_name] = dict(ts_borders)
        for point in top_ts_points:
            self._process_inp_node(point, None, 0)


    def _process_inp_node(self, inp_node, parent, depth):
        '''Recursive functmake
        ion that process hierarchical structure of timescale point
        add necessary information to self._timescales
        Args:
            (dict): point in timeseries
            (dict): parent point in timeseries
            (int): depth of point

        :param inp_node:

        :param parent:

        :param depth:

        :return:

        '''

        time_point = dict(depth=depth,
                          name_full=inp_node['name_full'],
                          name_short=inp_node['name_short'],
                          children=[])
        if parent is not None:
            parent['children'].append(time_point)
        self._timescales[depth]['timeline'].append(time_point)
        for child in inp_node['children']:
            self._process_inp_node(child, time_point, depth + 1)

    def _get_ts(self, ts_name):
        '''Search for timeseries by name in self._timescales attribute and return it
        Args:
            (string): ts_name - time series name
        Return:
            (list): time series content
        :param ts_name:
        :return:

        '''
        for ts in self._timescales:
            if ts['name'] == ts_name:
                index = self._timescales.index(ts)
                return ts, index
        raise ex.TlmNonExistentName(ts_name)

    def get_growth_lag(self, ts_name):
        '''Retuns timeseries growth_lag

        Args:
            (string): ts_name - time series name
        Return:
            (int): timeseries growth_lag

        :param ts_name:
        :return:

        '''

        ts = self._get_ts(ts_name)[0]
        return ts['growth_lag']

    def get_timeline_tree(self, top_ts_name, bottom_ts_name, period):
        '''Function process _timescale from top_ts_name to bottom_ts_name with period
        and build tree structure

        Args:
            (string): ts_name - time series name
            (string): bottom_ts_name - time series name
            (string): period - time series name
        Return:
            (dict): {top_ts_name:period}

        :param top_ts_name:

        :param bottom_ts_name:

        :param period:

        :return:

        '''

        # Declare outputs
        # tree - contains hierarchical structure for UI
        # borders - contains borders for every requested timescale

        tree = []
        borders = {top_ts_name: period}

        # Get top timescale
        top_ts = self._get_ts(top_ts_name)[0]

        # Get range of indexes for top timescale.
        start = self.get_index(top_ts_name, period[0])
        end = self.get_index(top_ts_name, period[1])

        # Get depth of search as index of bottom timescale
        max_depth = self._get_ts(bottom_ts_name)[1]

        # Loop points of top timescale inside of range.
        for i in range(start, end + 1):
            top_point = top_ts['timeline'][i]

            # Add top point to tree.
            tree.append(dict(
                id=top_point['name_full'],
                short_name=top_point['name_short'],
                full_name=top_point['name_full'],
                timescale=top_ts['name'],
                parent_index=None)
            )
            # Collect points from lower timescales recursively.
            # Define borders for every lower timescale.
            top_point_ind = len(tree) - 1
            for child in top_point['children']:
                self._add_point_to_tree(child, top_point_ind, max_depth, tree,
                                        borders)
        return tree, borders

    def _add_point_to_tree(self, point, parent_ind, max_depth, tree, borders):
        '''Function add specific point of timeseries to tree
        point, parent_ind, max_depth, tree, borders
        Args:
            (string): ts_name - time series name
            (string): bottom_ts_name - time series name
            (string): period - time series name

        Return:
            (dict): {top_ts_name:period}

        :param point:
        :param parent_ind:
        :param max_depth:
        :param tree:
        :param borders:
        :return:

        '''

        # Stop if point is too deep.
        if point['depth'] > max_depth:
            return
        # Add point to tree
        curr_ts_name = self._timescales[point['depth']]['name']
        tree.append(dict(short_name=point['name_short'],
                         full_name=point['name_full'],
                         timescale=curr_ts_name,
                         parent_index=parent_ind))
        # Update borders.
        curr_borders = borders.get(curr_ts_name)
        if curr_borders is None:
            borders[curr_ts_name] = (point['name_full'],
                                     point['name_full'])
        else:
            borders[curr_ts_name] = (borders[curr_ts_name][0],
                                     point['name_full'])
        # Collect points from lower timescales recursively.
        point_ind = len(tree) - 1
        for child in point['children']:
            self._add_point_to_tree(child, point_ind, max_depth, tree, borders)

    def get_names(self, ts_name, ts_period):
        '''Function return list of point in specific timeseries
        during specific period

        Args:
            (string): ts_name - time series name
            (string): ts_period

        Return:
            (list): names of point in timeseries

        :param ts_name:
        :param ts_period:
        :return:

        '''
        ts = self._get_ts(ts_name)[0]
        start = None
        end = None
        for index, point in enumerate(ts['timeline']):
            if point['name_full'] == ts_period[0]:
                start = index
            if point['name_full'] == ts_period[1]:
                end = index
        if start is None or end is None or start > end:
            raise PeriodOutOfRangeError
        return [x['name_full'] for x in ts['timeline'][start:end+1]]

    def get_time_length(self, ts_name):
        '''Count point in time series.

        Args:
            ts_name (string): time series name
        Returns:
            int: number of points in time series

        :param ts_name:
        :return:

        '''

        ts = self._get_ts(ts_name)[0]
        return len(ts['timeline'])

    def get_index(self, ts_name, label):
        '''Get point position in time series  by that name

        Args:
            (string): ts_name - time series name
            (string): label - full name of point in time series

        Return:
            (int): position in time series

        :param ts_name:
        :param label:
        :return:

        '''

        ts = self._get_ts(ts_name)[0]
        try:
            return [x['name_full'] for x in ts['timeline']].index(label)
        except ValueError:
            raise ex.TlmNonExistentLabel(ts_name, label)

    def get_label(self, ts_name, index):
        '''Get point's full name by given position in time series

        Args:
            (string): ts_name -  name of time series
            (int ):  label - position of point in time series

        Return:
            (string): name of point in time series

        :param ts_name:
        :param index:
        :return:

        '''

        ts = self._get_ts(ts_name)[0]
        try:
            return ts['timeline'][index]['name_full']
        except IndexError:
            raise ex.TlmNonExistentLabelIndex(ts_name, index)

    def get_period_by_alias(self, ts_name, period_alias):
        '''Return period time series by given period_alise

        Args:
            (string): ts_name - time series name
            (string): type of period alias

        Return:
            (tuple): (start_label,end_label),(start_index,end_index)
            start and and name of point in priod of time series, and start and and position of point in given period
            and timeseries


        :param ts_name:
        :param period_alias:
        :return:

        '''

        start_label, end_label = self._period_alias[period_alias][ts_name]
        start_index = self.get_index(ts_name, start_label)
        end_index = self.get_index(ts_name, end_label)
        return (start_label, end_label), (start_index, end_index)

    def get_timeline_by_period(self, ts_name, period):
        '''Return timeline points by timeline and
        start and end  of period.

        Args:
            (string): ts_name - time series name
            (string): period

        Return:
            (list): list of points name

        :param ts_name:
        :param period:
        :return:

        '''

        start_index = self.get_index(ts_name, period[0])
        end_index = self.get_index(ts_name, period[1])
        return [x['name_full'] for x in
                self._get_ts(ts_name)[0]['timeline'][start_index:end_index+1]]

    def get_last_actual(self, ts_name):
        '''Return name and intex of last point in
        history period of timeseries

        Args:
            (string): ts_names - name of timeseries

        Return :
            (tuple): border of timeseries and index of that point

        :param ts_name:
        :return:

        '''
        period, period_index = self.get_period_by_alias(ts_name, 'history')
        return period[1], period_index[1]

    def get_growth_periods(self, ts_name, period=None):
        '''Get list of of intervals for period in timeseries

        Args:
            (string): ts_names - name of
            (list): period - start and end of period

        Return :
            (list): list of tuples (start_interva,end_interval)

        :param ts_name:
        :param period:
        :return:

        '''
        # TODO rework (DR).
        if period is None:
            ts = self._get_ts(ts_name)[0]
            start = ts['timeline'][0]['name_full']
            end = ts['timeline'][-1]['name_short']
        else:
            start = period[0]
            end = period[1]

        periods = []
        #if ts_name == 'annual':
        start_ind = self.get_index(ts_name, start)
        end_ind = self.get_index(ts_name, end)
        for i in range(start_ind + 1, end_ind + 1):
            periods.append((self.get_label(ts_name, i - 1),
                            self.get_label(ts_name, i)))
        return periods


    def get_carg_periods(self, ts_name, ts_period=None):
        ts = self._get_ts(ts_name)[0]
        mid, mid_index = self.get_last_actual(ts_name)
        first, first_index = ts['timeline'][0]['name_full'], 0
        last, last_index = \
            ts['timeline'][-1]['name_full'], len(ts['timeline']) - 1
        if ts_period is not None:
            user_f, user_f_index = \
                ts_period[0], self.get_index(ts_name, ts_period[0])
            if user_f_index > first_index:
                first, first_index = user_f, user_f_index
            user_l, user_l_index = \
                ts_period[1], self.get_index(ts_name, ts_period[1])
            if user_l_index < last_index:
                last, last_index = user_l, user_l_index
        if first_index > mid_index or mid_index > last_index:
            raise WrongCargsPeriodError
        return [(first, mid), (mid, last)]
