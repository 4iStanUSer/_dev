class IProperties:
    pass

class Properties:
    pass

#@singleton
class IStorage:
    #there must be path for storing
    pass

class Storage(IStorage):
    pass

class IAdmin:

    def create_project(self,  project_name):

        new_project = Project(name= project_name)
        return new_project

    def delete_project(self, project_name):
        #delete project table from storage

    def get_project(self, project_name):
        #return project object from storage


    def get_projects(self):
        pass


    def get_properties(self, project_name):
        pass



class Project(Storage):

    def __init__(self, name):
        self.project_name=name


    def get_entities(self):
        pass

    def add_entities(self):
        pass

    def delete_entities(self):
        pass

    def save(self):
        pass


class Entity(Storage):

    def add_child(self):
        pass

    def get_child(self):
        pass

    def get_parents(self):
        pass

    def get_var(self):
        pass

    def del_var(self):
        pass

    def update_var(self):
        pass


class Variable(Storage):

    def add_ts(self):
        pass

    def get_ts(self):
        pass

class Timescale(Storage):

    def add_time_scale(self):
        pass

    def update_time_scale(self):
        pass

    def delete_update_time_scale(self):
        pass

class TimeSeries(Storage):

    def __init__(self):
        self.name

    def get_by_stamp(self):
        pass

    def get_by_index(self):
        pass

    def set_by_stamp(self):
        pass

    def set_by_index(self):
        pass





