from functools import reduce
from operator import mul
from math import fsum

from .base import CalculationBase


class CM_Sum(CalculationBase):
    # TODO add description

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        self.output[0] = fsum(self.input.get_all())
        return super().run()


class CM_Multiply(CalculationBase):
    # TODO add description

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        self.output[0] = reduce(mul, self.input.get_all(), 1)
        return super().run()


class CM_Divide(CalculationBase):
    # TODO add description

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        try:
            self.output[0] = self.input[0]/self.input[1]
        except ZeroDivisionError as e:
            raise e
        return super().run()
