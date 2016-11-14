from .base import CalculationBase


class CM_Delay(CalculationBase):
    # TODO add description

    def __init__(self):
        self._buffer_size = None
        self._prev_values = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._buffer_size = parameters.get('buffer_size')
        self._set_up()

    def run(self):
        # TODO add description
        try:
            index = self.runs_counter % self._buffer_size
            if self.runs_counter >= self._buffer_size:
                self.output[0] = self._prev_values[index]
            self._prev_values[index] = self.input[0]
        except ZeroDivisionError as e:
            raise e
        return super().run()

    def _set_up(self):
        self._prev_values = [0] * self._buffer_size


class CM_Switch(CalculationBase):

    def __init__(self):
        self._switch_number = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._switch_number = parameters.get('switch_number')

    def run(self):
        if self.runs_counter < self._switch_number:
            self.output[0] = self.input[0]
        else:
            self.output[0] = self.input[1]
        return super().run()


class CM_Growth(CalculationBase):

    def __init__(self):
        self._period_length = None
        self._var_type = None
        self._start_val = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._period_length = parameters.get('period_length')
        self._period_length -= 1
        self._var_type = parameters.get('var_type')

    def run(self):
        is_output = False
        if self.runs_counter == 0:
            self._start_val = self.input[0]
        elif self.runs_counter >= self._period_length:
            end_val = self.input[0]
            if self._var_type == 'abs':
                if self._start_val == 0:
                    self.output[0] = 0
                else:
                    self.output[0] = \
                        pow(end_val / self._start_val, self._period_length) - 1
            elif self._var_type == 'rate':
                self.output[0] = \
                    pow(end_val - self._start_val + 1, self._period_length) - 1
            else:
                raise Exception
            is_output = True
        super().run()
        return is_output



class CM_Impact(CalculationBase):
    # TODO add description
    def __init__(self):
        self._imp_type = None
        self._var_type = None
        self._sensitivity = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        # TODO add description
        super().set_parameters(parameters)
        self._imp_type = parameters.get('imp_type')
        self._var_type = parameters.get('var_type')
        self._sensitivity = parameters.get('sensitivity')

    def run(self):
        # TODO add description
        try:
            if self._var_type == 'abs':
                change = self.input[0] / self.input[1] - 1
            elif self._var_type == 'rate':
                change = self.input[0] - self.input[1]
            else:
                raise Exception
        except ZeroDivisionError:
            change = 0
        if self._imp_type == 'linear':
            self.output[0] = self._sensitivity * change
        elif self._imp_type == 'exp':
            self.output[0] = pow(change + 1, self._sensitivity) - 1
        else:
            raise Exception
        return super().run()


class CM_CumulativeSum(CalculationBase):

    def __init__(self):
        self._sum = 0

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._delay -= 2

    def run(self):
        self._sum += self.input[0]
        self.output[0] = self._sum
        return super().run()


class CM_CumulativeAverageLag(CalculationBase):

    def __init__(self):
        self._sum = 0

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def run(self):
        if self.runs_counter == 0:
            self.output[0] = 0
        else:
            self.output[0] = self._sum / self.runs_counter
        self._sum += self.input[0]
        return super().run()

class CM_ImpactAbove(CalculationBase):

    def __init__(self):
        self._imp_type = None
        self._above_count = None
        self._sensitivity = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        # TODO add description
        super().set_parameters(parameters)
        self._imp_type = parameters.get('imp_type')
        self._above_count = parameters.get('above_count')
        self._sensitivity = parameters.get('sensitivity')

    def run(self):
        try:
            total_change = self.input[0] / self.input[1] - 1
        except ZeroDivisionError:
            self.output[0] = 0
            return super().run()
        for i in range(self._above_count):
            try:
                change = self.input[2 * i + 2] / self.input[2 * i + 3] - 1
            except ZeroDivisionError:
                change = 0
            total_change -= change
        if self._imp_type == 'linear':
            self.output[0] = self._sensitivity * total_change
        elif self._imp_type == 'exp':
            self.output[0] = pow(total_change + 1, self._sensitivity) - 1
        else:
            raise Exception
        return super().run()


class CM_JJOralCare_DistributionImpact(CalculationBase):

    def __init__(self):
        self._sensitivity_regular = None
        self._sensitivity_innovations = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 2

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._sensitivity_regular = parameters.get('sensitivity_regular')
        self._sensitivity_innovations = \
            parameters.get('sensitivity_innovations')

    def run(self):
        self.output[0] = self._sensitivity_regular * \
                         ((self.input[0] * (1 - self.input[2]) -
                           self.input[1] * (1 - self.input[3])) / self.input[1])
        self.output[1] = self._sensitivity_innovations * \
                         ((self.input[0] * self.input[2] -
                           self.input[1] * self.input[3]) / self.input[1])
        return super().run()


class CM_JJOralCare_PriceImpact(CalculationBase):

    def __init__(self):
        self._sensitivity = None

    def clean(self):
        super().clean()
        self.__init__()

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self._sensitivity = parameters.get('sensitivity')

    def run(self):

        price_change = self.input[0] / self.input[1] - 1
        try:
            premium = self.input[2] / self.input[3] - 1
        except ZeroDivisionError:
            premium = 0
        try:
            inflation = self.input[4] / self.input[5] - 1
        except ZeroDivisionError:
            inflation = 0

        change = \
            price_change - premium - inflation - self.input[6] - \
            self.input[7] + self.input[8] + self.input[9]
        self.output[0] = pow(change + 1, self._sensitivity) - 1
        return super().run()


class CM_JJOralCare_DiscountOnPriceImpact(CalculationBase):

    @property
    def out_size(self):
        return 1

    def run(self):

        # 0 -- curr discount
        # 1 -- prev discount
        # 2 -- prev vol as promo
        # 3 -- due to discount

        self.output[0] = \
            (self.input[0]*self.input[3] + self.input[2]*(self.input[0]-self.input[1])) / (self.input[1]*self.input[2] - 1)
        return super().run()

class CM_JJOralCare_PromoOnPriceImpact(CalculationBase):

    @property
    def out_size(self):
        return 1

    def run(self):

        # 0 -- curr discount
        # 1 -- prev discount
        # 2 -- prev vol as promo
        # 3 -- due to support

        self.output[0] = \
            (self.input[0]*self.input[3]) / (self.input[1]*self.input[2] - 1)
        return super().run()
