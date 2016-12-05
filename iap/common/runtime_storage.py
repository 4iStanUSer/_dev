from threading import Lock

from ..common import exceptions as ex
from ..repository import persistent_storage
from ..forecasting.workbench import Workbench


class State:

    def __init__(self):
        self._user_id = None
        self._tool_id = 'common'
        self._project_id = None
        self._lang = 'en'

    @property
    def user_id(self):
        return self._user_id

    @property
    def tool_id(self):
        return self._tool_id

    @property
    def project_id(self):
        return self._project_id

    @property
    def language(self):
        return self._lang


class RunTimeStorage:

    def __init__(self):
        self._collection = {}
        self._lock = Lock()

    def get_wb(self, user_id):
        return self._get_user_box(user_id)['wb']

    def get_state(self, user_id):
        return self._get_user_box(user_id)['state']

    def update_state(self, user_id, **kwargs):
        user_box = self._get_user_box(user_id)
        if 'language' in kwargs.keys():
            with self._lock:
                user_box['state'] = kwargs['language']
        elif 'tool_id' and 'project_id' in kwargs.keys():
            old_tool_id = user_box['state'].tool_id
            old_project_id = user_box['state'].project_id
            if (old_tool_id != kwargs['tool_id']
                    or old_project_id != kwargs['project_id']):
                persistent_storage\
                    .save_backup(user_id, old_tool_id, old_project_id,
                                 user_box['wb'].get_backup())
                new_wb = self._load_wb(user_id, kwargs['tool_id'],
                                       kwargs['project_id'])
                with self._lock:
                    user_box['state'].tool_id = kwargs['tool_id']
                    user_box['state'].project_id = kwargs['project_id']
                    user_box['wb'] = new_wb
        else:
            raise Exception
        return

    def _get_user_box(self, user_id):
        user_box = self._collection.get(user_id)
        if user_box is None:
            state = self._load_state()
            wb = self._load_wb(state.user_id, state.tool_id, state.project_id)
            user_box = dict(state=state, wb=wb)
            with self._lock:
                self._collection[user_id] = user_box
            return user_box

    @staticmethod
    def _load_state(self):
        return State()

    def _load_wb(self, user_id, tool_id, project_id):
        # Load backup
        backup = persistent_storage.load_backup(user_id, tool_id, project_id,
                                                'default')
        if backup is None:
            raise ex.BackupNotFoundError(user_id, tool_id, project_id)
        wb_class = self._get_wb_class_by_tool(tool_id)
        if wb_class is None:
            raise ex.UnknownToolError(tool_id)
        wb = wb_class(user_id)
        wb.load_from_backup(backup)
        return wb

    @staticmethod
    def _get_wb_class_by_tool(tool_id):
        if tool_id == 'forecast':
            return Workbench
        return None



