class PersistentStorage:
    def get_user_tools_with_projects(self, user_id):
        return ['forecast'], ['JJOralCare']

    def get_project(self, **kwargs):

        class TmpProject:
            def __init__(self):
                self.id = 'JJOralCare'
                self.tool_id = 'forecast'

        return TmpProject()



