from .base import CalculationBase

class CM_AutoSum(CalculationBase):

    # TODO add description
    def __init__(self):
        self.runs_counter = 0
        self.order = None
        self.prev_values = None

    def load_parameters(self, parameters):
        # TODO add description
        try:
            self.order = int(parameters['order'])
            self.prev_values = [0] * self.order
        except KeyError:
            raise Exception
            # TODO define custom exception
        except ValueError:
            raise Exception
            # TODO define custom exception

    def run(self):
        # TODO add description
        index = self.runs_counter % self.order
        if self.runs_counter < self.order:
            self.prev_values[index] = self.input[0]
        self.output[0] = self.prev_values[index] * (1+self.input[1])
        self.prev_values[index] = self.output[0]
        self.runs_counter += 1


class CM_AdStockSimple(CalculationBase):

    def __init__(self):
        self.runs_counter = 0
        self.media_sum = 0
        self.lag = None
        self.accumulation = None
        self.ini_values = None
        self.calc_values = None
        pass

    def load_parameters(self, parameters):
        try:
            self.lag = int(parameters['lag'])
            self.accumulation = int(parameters['accumulation'])
            self.ini_values = []
            self.calc_values = [0] * self.lag
            self.delay = self.lag
        except KeyError:
            raise Exception
            # TODO define custom exception
        except ValueError:
            raise Exception
            # TODO define custom exception

    def run(self):
        self.runs_counter += 1
        # Accumulation
        oldest = 0
        newest = self.input[0]
        if self.runs_counter > self.accumulation:
            oldest = self.ini_values.popleft()
        self.ini_values.append(newest)
        self.media_sum = self.media_sum - oldest + newest
        # Lag
        index = (self.runs_counter-1) % self.lag
        if self.runs_counter >= self.delay:
            self.output[0] = self.calc_values[index]
        self.calc_values[index] = self.media_sum


class CM_DiscountImpact(CalculationBase):

    def run(self):
        self.output[0] = pow(1 - self.input[0], self.input[1])


class CM_PromoCalculator(CalculationBase):

    def __init__(self):
        self.ppe = None
        self.qm_lift = None
        self.promo_discount = None
        self.promo_support = None

    def load_parameters(self, parameters):
        try:
            self.ppe = parameters['PPE']
            self.qm_lift = parameters['QM Lift']
            self.promo_discount = parameters['Promotion Discount']
            self.promo_support = parameters['Promotion Support']
        except KeyError:
            raise Exception
            # TODO define custom exception
        except ValueError:
            raise Exception
            # TODO define custom exception

    def run(self):
        pass

    # 0: Number of weeks in month
    #'Modeled Base Units'
    #Display
    #Promotion
    #Display parameters - string
    #Promo parameters - string

class CM_Delay_Switch(CalculationBase):
    # TODO add description
    def __init__(self):
        self._runs_counter = 0
        self.prev_value = 0

    def clean(self):
        pass

    @property
    def out_size(self):
        return 1

    def set_parameters(self, parameters):
        self._delay = parameters.get('delay', 0)
        self.__init__()

    def run(self):
        if self.runs_counter == 0:
            self.prev_value = self.input[0]
        elif self.runs_counter == 1:
            self.output[0] = self.prev_value
        else:
            self.output[0] = self.input[1]
        self.runs_counter += 1

    def clean(self):
        self.__init__()


