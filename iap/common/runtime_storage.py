from threading import Lock

from ..common import exceptions as ex
from .repository import persistent_storage
from ..forecasting.workbench import *


class State:

    def __init__(self, user_id):
        self._user_id = user_id
        self._tool_id = None
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
    @property
    def isempty(self):
        if self._tool_id==None and self._project_id == None:
            return True
        else:
            return False


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
                user_box['state']._lang = kwargs['language']
        elif 'tool_id' and 'project_id' in list(kwargs.keys()):
            new_tool = kwargs['tool_id']
            new_proj = kwargs['project_id']
            old_tool = user_box['state'].tool_id
            old_proj = user_box['state'].project_id
            if old_tool != new_tool or old_proj != new_proj:
                if old_tool is not None and old_proj is not None:
                    persistent_storage\
                        .save_backup(user_id, old_tool, old_proj,
                                     user_box['wb'].get_backup())
                new_wb = self._load_wb(user_id, new_tool, new_proj)
                with self._lock:
                    user_box['state']._tool_id = new_tool
                    user_box['state']._project_id = new_proj
                    user_box['wb'] = new_wb
        else:
            raise Exception
        return

    def _get_user_box(self, user_id):
        user_box = self._collection.get(user_id)
        if user_box is None and self._load_state(user_id) is None:
            pass
        if user_box is None:
            state = self._load_state(user_id)
            wb = self._load_wb(state.user_id, state.tool_id, state.project_id)
            user_box = dict(state=state, wb=wb)
            with self._lock:
                self._collection[user_id] = user_box
        return user_box

    def _load_state(self, user_id):
        return State(user_id)

    def _load_wb(self, user_id, tool_id, project_id):
        if tool_id is None or project_id is None:
            tool_id = 1
            project_id=1

        # Load backup
        backup = persistent_storage.load_backup(user_id, tool_id, project_id, 'default')
        if backup is None:
            raise ex.BackupNotFoundError(user_id, tool_id, project_id)
        wb_class = self._get_wb_class_by_tool(tool_id)
        if wb_class is None:
            raise ex.UnknownToolError(tool_id)
        wb = wb_class(user_id)
        wb.load_from_backup(backup, None)
        return wb

    @staticmethod
    def _get_wb_class_by_tool(tool_id):
        if tool_id == 'forecast':
            return Workbench
        elif tool_id == 1:
            return Workbench
        return None

    ######


