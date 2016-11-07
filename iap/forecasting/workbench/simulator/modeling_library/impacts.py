from math import pow

from .base import CalculationBase


class CM_LinearImpact(CalculationBase):
    # TODO add description

    def run(self):
        # TODO add description
        try:
            self.output[0] = self.input[0] * (self.input[1]/self.input[2] - 1)
        except ZeroDivisionError as e:
            raise e


class CM_ExponentialImpact(CalculationBase):

    def run(self):
        # TODO add description
        try:
            self.output[0] =\
                pow(self.input[1]/self.input[2], self.input[0]) - 1
        except ZeroDivisionError as e:
            raise e

class CM_Impact(CalculationBase):
    # TODO add description
    def __init__(self, immutable_parameters):
        try:
            self.imp_type = immutable_parameters['type']
            self.var_type = immutable_parameters['var_type']
            self.sensitivity = None
        except KeyError:
            raise Exception

    def set_parameters(self, mutable_parameters):
        # TODO add description
        try:
            self.sensitivity = mutable_parameters[0]
        except IndexError:
            raise Exception

    def run(self):
        # TODO add description
        try:
            if self.var_type == 'abs':
                change = self.input[0] / self.input[1] - 1
            elif self.var_type == 'rate':
                change = self.input[0] - self.input[1]
            else:
                raise Exception
        except ZeroDivisionError:
            change = 0
        if self.imp_type == 'linear':
            self.output[0] = self.sensitivity * change
        elif self.imp_type == 'exp':
            self.output[0] = pow(change + 1, self.sensitivity) - 1
        else:
            raise Exception
        kk = self.output[0]
        return


class CM_ImpactAbove(CalculationBase):

    def __init__(self, immutable_parameters):
        try:
            self.imp_type = immutable_parameters['type']
            self.above_count = immutable_parameters['above_count']
            self.sensitivity = None
        except IndexError:
            raise Exception

    def set_parameters(self, mutable_parameters):
        # TODO add description
        try:
            self.sensitivity = mutable_parameters[0]
        except IndexError:
            raise Exception

    def run(self):
        try:
            total_change = self.input[0] / self.input[1] - 1
        except ZeroDivisionError:
            self.output[0] = 0
            return
        for i in range(self.above_count):
            try:
                change = self.input[2 * i + 2] / self.input[2 * i + 3] - 1
            except ZeroDivisionError:
                change = 0
            total_change -= change
        if self.imp_type == 'linear':
            self.output[0] = self.sensitivity * change
        elif self.imp_type == 'exp':
            self.output[0] = pow(change + 1, self.sensitivity) - 1
        else:
            raise Exception
        kk = self.output[0]
        return


class CM_JJOralCare_DistributionImpact(CalculationBase):

    def __init__(self, immutable_parameters=None):
        self.sensitivity_regular = None
        self.sensitivity_innovations = None

    def set_parameters(self, mutable_parameters):
        # TODO add description
        try:
            self.sensitivity_regular = mutable_parameters[0]
            self.sensitivity_innovations = mutable_parameters[1]
        except IndexError:
            raise Exception

    def run(self):
        self.output[0] = self.sensitivity_regular * \
                         ((self.input[0] * (1 - self.input[2]) -
                           self.input[1] * (1 - self.input[3])) / self.input[0]) + \
                         self.sensitivity_innovations * \
                         ((self.input[0] * self.input[2] -
                           self.input[1] * self.input[3]) / self.input[0])
        kk = self.output[0]
        return


class CM_JJOralCare_PriceImpact(CalculationBase):
    def __init__(self, immutable_parameters=None):
        self.sensitivity = None

    def set_parameters(self, mutable_parameters):
        # TODO add description
        try:
            self.sensitivity = mutable_parameters[0]
        except IndexError:
            raise Exception

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
        above = self.input[6]

        self.output[0] = pow(price_change - premium - inflation + above + 1,
                             self.sensitivity) - 1
        kk = self.output[0]
        return
