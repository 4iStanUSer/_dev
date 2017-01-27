class IStorage:

    def __init__(self, backup, template):
        self.backup = backup
        self.template = template


class IBackup:

    def __init__(self, storage):
        self.storage = storage

    def save(self, user_id, tool_id, data_to_save, backup_name='default'):
        self.storage.save_backup(user_id, tool_id, data_to_save, backup_name)

    def delete(self, user_id, tool_id, backup_name):
        self.storage.delete_backup(user_id, tool_id, backup_name)

    def get(self, user_id, tool_id, backup_name):
        return self.storage.load_backup(user_id, tool_id, backup_name)

    def get_list(self, user_id, tool_id):
        users_ids = [user_id]
        # TODO
        # here should be used a function that gets
        # all users IDs available for current user
        # according to user's permission
        return self.storage.get_available_backups_info(users_ids, tool_id)


class ITemplate:

    def __init__(self, storage):
        self.storage = storage

    def save(self, tool_id, data_to_save, tpl_name='default_tpl'):
        self.storage.save_template(tool_id, data_to_save, tpl_name)

    def get(self, tool_id, tpl_name):
        self.storage.load_template(tool_id, tpl_name)

    def delete(self, tool_id, tpl_name):
        self.storage.delete_template(tool_id, tpl_name)
