class CalculationBase:
    """
    Base class for modules
    """

    def __new__(cls, *args, **kwargs):
        obj = super(CalculationBase, cls).__new__(cls)
        obj._input = None
        obj._output = None
        obj._delay = 0
        obj._runs_counter = 0
        return obj

    def __init__(self):
        pass

    def set_input_buffer(self, buffer, indxs):
        """ Marking input indexes in buffer
        """
        self._input = RelativeBuffer(buffer, indxs)

    def set_output_buffer(self, buffer, indxs):
        """ Marking output indexes in buffer
        """
        self._output = RelativeBuffer(buffer, indxs)

    @property
    def input(self):
        # TODO add description
        return self._input

    @property
    def output(self):
        # TODO add description
        return self._output

    @property
    def delay(self):
        # TODO add description
        return self._delay

    @property
    def runs_counter(self):
        return self._runs_counter

    @property
    def out_size(self):
        # TODO add description
        raise NotImplementedError

    def run(self):
        # TODO add description
        self._runs_counter += 1
        return self._runs_counter > self._delay

    def set_parameters(self, parameters):
        # TODO add description
        self._delay = parameters.get('delay', 0)

    def clean(self):
        self._runs_counter = 0


class RelativeBuffer:
    """ Work with buffer
    """
    def __init__(self, buffer, indxs):
        self._buffer = buffer
        self._indxs = list(indxs)

    def __getitem__(self, pos):
        return self._buffer[self._indxs[pos]]

    def __setitem__(self, pos, value):
        self._buffer[self._indxs[pos]] = value

    def __len__(self):
        return len(self._indxs)

    def get_all(self):
        """ Return list of values from buffer by indexes
        """
        return [self._buffer[x] for x in self._indxs]
