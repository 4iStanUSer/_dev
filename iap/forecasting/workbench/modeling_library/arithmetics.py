from functools import reduce
from operator import mul
from math import fsum

from .base import CalculationBase


class CM_Sum(CalculationBase):
    """
    Return an accurate floating point sum of values in input
    :return:
    :rtype: float
    """

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        try:
            self.output[0] = fsum(self.input.get_all())
        except:
            # TODO handle complex values
            self.output[0] = 0
        return super().run()


class CM_Multiply(CalculationBase):
    """
    Return an accurate floating point product of values in input
    :return:
    :rtype: float
    """

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        self.output[0] = reduce(mul, self.input.get_all(), 1)
        return super().run()


class CM_Divide(CalculationBase):
    """
    Return result of division of first value on second value from input
    :return:
    :rtype:
    """

    @property
    def out_size(self):
        return 1

    def run(self):
        # TODO add description
        try:
            self.output[0] = self.input[0]/self.input[1]
        except ZeroDivisionError as e:
            # TODO handle division by zero
            # raise e
            self.output[0] = 0
        return super().run()
