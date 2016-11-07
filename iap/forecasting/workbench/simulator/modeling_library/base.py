class CalculationBase:
    # TODO add description
    def __new__(cls, *args, **kwargs):
        obj = super(CalculationBase, cls).__new__(cls)
        obj._input = None
        obj._output = None
        obj._delay = 0
        return obj

    def __init__(self, immutable_parameters=None):
        pass

    def set_input_buffer(self, buffer, indxs):
        # TODO add description
        self._input = RelativeBuffer(buffer, indxs)

    def set_output_buffer(self, buffer, indxs):
        # TODO add description
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

    def run(self):
        # TODO add description
        raise NotImplementedError

    def load_parameters(self, parameters):
        # TODO add description
        raise NotImplementedError

    def get_parameters_for_save(self):
        # TODO add description
        raise NotImplementedError

    def clean(self):
        pass


class RelativeBuffer:
    # TODO add description
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
        return [self._buffer[x] for x in self._indxs]