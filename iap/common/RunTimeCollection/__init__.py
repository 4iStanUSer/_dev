from . import exceptions as ex


class RunTimeCollection:
    saved = {}

    def add(self, user_id, instance):
        if user_id not in self.saved:
            self.saved[user_id] = instance
        else:
            raise ex.InstanceAlreadyExistsError(user_id)

    def delete(self, user_id):
        if user_id in self.saved:
            del self.saved[user_id]

    def get(self, user_id):
        instance = self.saved[user_id]
        return instance
