from . import exceptions as ex
from iap.repository.storage import *


class RunTimeCollection:
    saved = {}

    def __init__(self, tool_name):
        self.tool_name = tool_name

    def add(self, user_id, instance):
        if user_id not in self.saved:
            self.saved[user_id] = instance
        else:
            raise ex.InstanceAlreadyExistsError(user_id)

    def delete(self, user_id):
        if user_id in self.saved:
            del self.saved[user_id]

    def get(self, user_id):
        if user_id in self.saved:
            instance = self.saved[user_id]
        else:
            instance = self.__lookup_in_storage(user_id)
            self.add(user_id, instance)
        return instance

    def __lookup_in_storage(self, user_id):
        s = Storage()
        data = s.load_backup(user_id, self.tool_name, 'default')
        if data:
            instance = self.__create_instance(self.tool_name)
            instance.load(data)
            return instance
        else:
            raise ex.BackupNotFound(user_id, self.tool_name)

    def __create_instance(self, tool_name):
        if tool_name == 'forecasting':
            instance = ForecastForDemoInstance()
        else:
            raise ex.InstanceCanNotBeCreated(tool_name)
        return instance


class ForecastForDemoInstance:
    data = {}

    def load(self, data):
        self.data = data
