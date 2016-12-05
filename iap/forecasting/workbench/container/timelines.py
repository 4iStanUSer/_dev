import copy
from .. import exceptions as ex

class TimeLineManager:

    def __init__(self):
        self._timescales = []
        self._period_alias = dict()

    def get_backup(self):
        return dict(timescales=self._timescales, alias=self._period_alias)

    def load_backup(self, backup):
        self._timescales = backup['timescales']
        self._period_alias = backup['alias']

    def load_timelines(self, ts_properties, alias, top_ts_points):
        self._timescales = \
            [dict(name=name, growth_lag=props['growth_lag'], timeline=[])
             for name, props in ts_properties.items()]
        for period_name, ts_borders in alias.items():
            self._period_alias[period_name] = dict(ts_borders)
        for point in top_ts_points:
            self._process_inp_node(point, None, 0)

    def _process_inp_node(self, inp_node, parent, depth):
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
        for index, ts in enumerate(self._timescales):
            if ts['name'] == ts_name:
                return ts, index
        raise ex.TlmNonExistentName(ts_name)

    def get_growth_lag(self, ts_name):
        ts = self._get_ts(ts_name)[0]
        return ts['growth_lag']

    def get_timeline_tree(self, top_ts_name, bottom_ts_name, period):
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
        for child in point.children:
            self._add_point_to_tree(child, point_ind, max_depth, tree, borders)

    def get_names(self, ts_name, ts_period):
        ts = self._get_ts(ts_name)[0]
        start = None
        end = None
        for index, point in enumerate(ts['timeline']):
            if point['name_full'] == ts_period[0]:
                start = index
            if point['name_full'] == ts_period[1]:
                end = index
        if start is None or end is None or start > end:
            raise Exception
        return [x['name_full'] for x in ts['timeline'][start:end+1]]

    def get_time_length(self, ts_name):
        ts = self._get_ts(ts_name)[0]
        return len(ts['timeline'])

    def get_index(self, ts_name, label):
        ts = self._get_ts(ts_name)[0]
        try:
            return [x['name_full'] for x in ts['timeline']].index(label)
        except ValueError:
            raise ex.TlmNonExistentLabel(ts_name, label)

    def get_label(self, ts_name, index):
        ts = self._get_ts(ts_name)[0]
        try:
            return ts['timeline'][index]['name_full']
        except IndexError:
            raise ex.TlmNonExistentLabelIndex(ts_name, index)

    def get_period_by_alias(self, ts_name, period_alias):
        start_label, end_label = self._period_alias[period_alias][ts_name]
        start_index = self.get_index(ts_name, start_label)
        end_index = self.get_index(ts_name, end_label)
        return (start_label, end_label), (start_index, end_index)

    def get_timeline_by_period(self, ts_name, period):
        start_index = self.get_index(ts_name, period[0])
        end_index = self.get_index(ts_name, period[1])
        return [x['name_full'] for x in
                self._get_ts(ts_name)[0]['timeline'][start_index:end_index+1]]

    def get_last_actual(self, ts_name):

        period, period_index = self.get_period_by_alias(ts_name, 'history')
        return period[1], period_index[1]

    def get_growth_periods(self, ts_name, period=None):
        # TODO rework (DR).
        if period is None:
            ts = self._get_ts(ts_name)[0]
            start = ts['timeline'][0]['name_full']
            end = ts['timeline'][-1]['name_short']
        else:
            start = period[0]
            end = period[1]

        periods = []
        if ts_name == 'annual':
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
            raise Exception
        return [(first, mid), (mid, last)]
