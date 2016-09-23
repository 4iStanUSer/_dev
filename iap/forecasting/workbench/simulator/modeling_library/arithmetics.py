from functools import reduce
from operator import mul
from math import fsum

from .base import CalculationBase


class CM_Sum(CalculationBase):
    # TODO add description
    def run(self):
        # TODO add description
        self.output[0] = fsum(self.input)


class CM_Multiply(CalculationBase):
    # TODO add description
    def run(self):
        # TODO add description
        self.output[0] = reduce(mul, self.input, 1)


class CM_Divide(CalculationBase):
    # TODO add description
    def run(self):
        # TODO add description
        try:
            self.output[0] = self.input[0]/self.input[1]
        except ZeroDivisionError as e:
            raise e
