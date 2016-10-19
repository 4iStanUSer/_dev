from threading import Lock

from ..common import exceptions as ex
from ..repository import persistent_storage
from ..forecasting.workbench import Workbench
import copy


class State:

    def __init__(self):
        self.user_id = None
        self.tool_id = None
        self.project_id = None


class RunTimeStorage:

    def __init__(self):
        self._collection = {}
        self._lock = Lock()

    def get_wb(self, user_id, tool_id):
        user_box = self._collection.get(user_id, None)
        if user_box is None:
            raise ex.UserNotFoundError
        if user_box['state'].tool_id != tool_id:
            raise ex.WrongToolError(tool_id, user_box['state'].tool_id)
        return user_box['wb']

    def set_state(self, state):
        user_box = self._collection.get(state.user_id, None)
        if user_box is None:
            wb = self._get_wb_from_storage(state)
            user_box = dict(state=copy.copy(state), wb=wb)
            with self._lock:
                self._collection[state.user_id] = user_box
        else:
            # TODO Add realization (DR)
            raise NotImplementedError
        return

    def _get_wb_from_storage(self, state):
        # Check state
        if (state.user_id is None or state.tool_id is None or
                state.project_id is None):
            raise ex.InvalidStateError(state)
        # Load backup
        backup = persistent_storage.load_backup(state.user_id, state.tool_id,
                                                state.project_id, 'default')
        if backup is None:
            raise ex.BackupNotFoundError(state.user_id, state.tool_id,
                                         state.project_id)
        wb_class = self._get_wb_class_by_tool(state.tool_id)
        if wb_class is None:
            raise ex.UnknownToolError(state.tool_id)
        wb = wb_class(state.user_id)
        wb.load_backup(backup)
        return wb

    @staticmethod
    def _get_wb_class_by_tool(tool_id):
        if tool_id == 'forecast':
            return Workbench
        return None







