class TimeLineManager:

    def __init__(self):
        self.time_scales = {}

    def add_time_line(self, ts_name, time_line):
        self.time_scales[ts_name] = list(time_line)

    def get_time_length(self, ts_name):
        try:
            return len(self.time_scales[ts_name])
        except KeyError:
            raise Exception
    def get_index_by_label(self, ts_name, label):
        try:
            return self.time_scales[ts_name].index(label)
        except ValueError:
            raise Exception
        except KeyError:
            raise Exception

    def get_label_by_index(self, ts_name, index):
        try:
            return self.time_scales[ts_name][index]
        except IndexError:
            raise Exception
        except KeyError:
            raise Exception
