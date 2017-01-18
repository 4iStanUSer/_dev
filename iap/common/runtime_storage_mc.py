from .runtime_storage import State
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

class RuntimeStorage():
    """
    Runtime Storage realised over memcahed
    """
    def __init__(self):

        self.client = []
        self.client = memcache.Client(['127.0.0.1:11211'], debug=0)

    def update_state(self, user_id, state):
        #pass

    def set_new_user_box(self, user_id, tool_id, project_id):
        pass

    def end_state(self):
        pass

    def get_user_box(self):
        pass
