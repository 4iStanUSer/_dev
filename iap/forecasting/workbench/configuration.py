import copy


class Configuration(dict):

    def load(self, data):
        self.clear()
        for key, value in data.items():
            self.__setitem__(key, copy.copy(value))

    def save(self):
        return copy.copy(self)




