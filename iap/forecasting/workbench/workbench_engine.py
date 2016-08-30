from .container import Container
from .access import Access
from .dimensions import Dimensions
from .configuration import Configuration

from ...repository import get_wh_interface  # TODO REMOVE


class WorkbenchEngine:
    def __init__(self, user_id, imanage_access, ssn):  # TODO DELETE SSN
        self._user = user_id
        user = imanage_access.get_user(ssn, id=self._user)
        self._user_roles = [x.id for x in user.roles]

        self.loaded = False

        self.container = Container()
        self.kernel = None

        self.config = Configuration()
        self.access = Access(self._user, self._user_roles)
        self.dimensions = Dimensions()

    def load_data_from_repository(self, warehouse):
        pass

    def load_backup(self, backup):  # TODO remove imanage_acc
        self.loaded = True

        config = backup.get('configuration') \
            if 'configuration' in backup else dict()
        access = backup.get('access') \
            if 'access' in backup else dict()
        # dimensions = backup.get('dimensions') \
        #     if 'dimensions' in backup else dict()
        wh = get_wh_interface()

        self.config.load(config)  # TODO clean
        self.access.load(access)  # TODO clean
        self.dimensions.load(wh.get_entity_by_id(1))  # TODO clean

        return True

    def get_data_for_backup(self):
        config = self.config.save()
        access = self.access.save()
        dimensions = self.dimensions.save()

        return {
            'configuration': config,
            'access': access,
            'dimensions': dimensions
        }
