from ..container import exceptions as ex

class ConfigManager():
    '''
    Contains data related configuration of container.
    '''

    def __init__(self):
        self.timescales = ['annual']
        self.dimensions = {'geography': ['country'], 'product': ['category']}

    def get_container_config(self):
        pass

    def get_point_config(self, coordinates):
        point_config = {}
        point_config['time_len'] = 7
        point_config['var_names'] = ['Sales Value',
                                     'Sales Volume',
                                     'Avg Price per Eq',
                                     'Sales Unit',
                                     'Price per Unit',
                                     'Unit Size',
                                     'Distribution',
                                     'Innovations share',
                                     'Advertising',
                                     'Premiumization',
                                     'Avg Branded Discount',
                                     'Avg Promo Support',
                                     'Category Long Term Trend',
                                     'CPI', 
                                     'Real GDP per capita', 
                                     'Population total',
                                     'Sensitivity to Population Growth',
                                     'Sensitivity to GDP PC',
                                     'Innovations Sensitivity',
                                     'Incrementality of Distribution',
                                     'Unit Price Elasticity',
                                     'Unit Size Elasticity',
                                     'Sensitivity to Advertising',
                                     'Sensitivity to Trade & Promo',
                                     'Sensitivity to Inflation']
        return point_config

'''
class VariableRule:

    def __init__(self, timescale):
        self.__timescale = timescale
        self.__dimensions = {}
        self.__rule = {}

    def set_selector(self, selector):
        self.__dimensions = selector.copy()

    def set_rule(self, rules):
        for key, value in rules:
            for var in value:
                self.__rule[var] = key
'''