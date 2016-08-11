class Warehouse:
    @staticmethod
    def get(address):
        entity = Entity()
        return entity


class Entity:
    @staticmethod
    def force_data_by_name(name):
        variable = Variable()
        return variable


class Variable:
    @staticmethod
    def force_series(name):
        times_series = TimeSeries()
        return times_series


class TimeSeries:
    @staticmethod
    def get():
        return None

    @staticmethod
    def set_data(start_point, values):
        start_point = start_point
        values = values

    @staticmethod
    def get_by_point(date_point, num_of_values):
        result = [0] * num_of_values
        return result
