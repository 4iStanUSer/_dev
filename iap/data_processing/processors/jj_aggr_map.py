from iap.repository.warehouse import exceptions as ex


def data_aggr_processor(proc_data):
    aggr = DataAggregate(proc_data, dates_souce='weekly', 
                         dates_target='monthly')


class DataAggregate:
    dates_source = ''
    dates_target = ''

    def __init__(self, data, sum_rules, map_rules, **kwargs):
        '''
        Args: 
        - data (obligatory)
        - source dates type(dates_source): daily, weekly, monthly, etc.
        - target dates type(dates_target): weekly, monthly, year, etc.
        '''
        if data is None:
            raise ex.EmptyInputsError('No data to work with')
        self.data = data
        self.sum_rules = sum_rules
        self.map_rules = map_rules
        for key, val in kwargs.items():
            if key == 'dates_source':
                self.dates_source = val
            if key == 'dates_target':
                self.dates_target = val
        self.sum_func_map = {'average': self.__average_sum,
                             'sum': self.__simple_sum}

    def meta_map_by_rules(self):
        for row in self.data:
            for rule in self.map_rules:
                # Looking for rules match
                is_matched = True
                for meta_name, val in rule['in'].items():
                    if row['meta'][meta_name] != val:
                        is_matched = False
                        break
                if is_matched:
                    # Write updated info
                    for meta_name, val in rule['out'].items():
                        row['meta'][meta_name] = val
        return self.data

    def sum_by_meta(self):
        new_output = []
        new_row = self.data_sum_by_rules(
            [self.data[1], self.data[2], self.data[3]], self.sum_rules)
        new_output.append({'meta': self.data[1]['meta'],
                           'dates': self.data[1]['dates'], 'data': new_row})
        return new_output

    def data_sum_by_rules(self, data_rows, sum_rules):
        output = {}
        # Read data col names
        for col_name, value in data_rows[0]['data'].items():
            col_found = False
            # All data rows must have rules for sum
            for rule_item in sum_rules:
                if rule_item['Name'].lower() == col_name.lower():
                    rule_name = rule_item['FactScale'].lower()
                    col_found = True
                    if rule_name in self.sum_func_map:
                        sum_method = self.sum_func_map[rule_name]
                    else:
                        raise ex.EmptyInputsError('No function match to the\
                        sum method')
                    break
            if not col_found:
                raise ex.EmptyInputsError('No sum rule fot the data column ' 
                                          + str(col_name))
            # sum all rows that has col_name
            sum_data = []
            for row in data_rows:
                data_value = row['data'][col_name]
                sum_data.append(data_value)
            result = sum_method(sum_data)
            output[col_name] = result
        return output

    def __average_sum(self, sum_data):
        '''
        sum_data - list of numeric data
        if val is string - return 'N/A' as sum result
        '''
        sum = 0.0
        counter = 0
        for val in sum_data:
            if type(val) is str:
                return 'N/A'
            counter = counter + 1
            sum = sum + val
        if sum == 0 or counter == 0:
            result = 0
        else:
            result = sum/counter
        return result

    def __simple_sum(self, sum_data):
        '''
        sum_data - list of numeric data
        if val is string - return 'N/A' as sum result
        '''
        sum = 0.0
        for val in sum_data:
            if type(val) is str:
                return 'N/A'
            sum = sum + val
        return sum
