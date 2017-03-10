import pandas as pd
import logging
logging.getLogger(__name__)


class Warehouse:
    """
    Warehouse class used for

    :return:
    :rtype:
    """
    def __init__(self):
        self.data_frame = pd.DataFrame()

    def set_config(self, format=None, path=None , sheet_name = None):

        self.format = format
        self.path = path
        self.sheet_name = sheet_name
        pass

    def load_data_set(self):
        if self.format == '.csv':
            self.data_frame.to_csv()
        elif self.format==".xlsx":
            self.data_frame.to_excel()
        elif self.format=='.json':
            pass
        else:
            pass

    def save_file(self):
        if self.format == '.csv':
            self.data_frame.to_csv()
        elif self.format==".xlsx":
            self.data_frame.to_excel()
        elif self.format=='.json':
            pass
        else:
            pass

    def get_shape(self, ):
        return self.data_frame.shape

    def get_columns(self):
        return self.data_frame.columns

    def data_by_condition(self, confition:str):
        pass

    def get_columns(self, columns):
        return self.data_frame[columns]

    def add_columns(self, column_name, values):
        try:
            self.data_frame[column_name] = values
        except ValueError:
            return None

    def delete_column(self, column_name):
        try:
            del self.data_frame[column_name]
        except KeyError:
            return None

    def update_column(self, column_name, values, start_index):
        for i in range(start_index, start_index+len(values)):
            self.data_frame.loc[i:i, column_name:column_name] = values[i]

    def get_rows(self, start_row, end_row):
        return self.data_frame.loc[start_row:end_row]

    def add_row(self, row):
        pass

    def get_cell(self, collumn_name, row_name):
        return self.data_frame.loc[row_name:row_name, collumn_name:collumn_name]

    def update_cell(self, column_name, row_name, value):
        self.data_frame.loc[row_name:row_name, column_name:column_name] =value

    def drop_dublicate(self):
        pass

    def group_by(self, parameter, aggr_function):
        pass

    def fill_na(self):
        pass