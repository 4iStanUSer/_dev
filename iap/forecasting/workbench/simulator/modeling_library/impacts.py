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
