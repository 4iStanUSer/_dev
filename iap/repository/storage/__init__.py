import os
import pickle
import datetime

from . import exceptions as ex

FILE_EXTENSION = '.pickle'
BACKUP_STORAGE_PATH = 'for_backup_storage'
TPL_STORAGE_PATH = 'for_tpl_storage'
CONFIG_STORAGE_PATH = 'for_config_storage'


class Storage:
    def save_backup(self, user_id, tool_id, data_to_save, backup_name='default'):
        if not os.path.exists(self.__get_user_backup_dir_path(user_id, tool_id)):
            os.makedirs(self.__get_user_backup_dir_path(user_id, tool_id))
        file_path = self.__get_backup_file_path(user_id, tool_id, backup_name)
        file_info = {
            'name': backup_name,
            'user_id': user_id,
            'date': datetime.datetime.now()
        }
        self.__save(file_path, file_info, data_to_save)

    def save_template(self, tool_id, data_to_save, tpl_name='default_tpl'):
        if not os.path.exists(self.__get_tpl_dir_path(tool_id)):
            os.makedirs(self.__get_tpl_dir_path(tool_id))
        file_path = self.__get_tpl_file_path(tool_id, tpl_name)
        file_info = {
            'name': tpl_name,
            'date': datetime.datetime.now()
        }
        self.__save(file_path, file_info, data_to_save)

    @staticmethod
    def __save(file_path, file_info, data_to_save):

        data_with_info = {
            'data': data_to_save,
            'info': file_info
        }
        with open(file_path, 'wb') as f:
            pickle.dump(data_with_info, f, pickle.HIGHEST_PROTOCOL)

    def load_backup(self, user_id, tool_id, backup_name):
        file_path = self.__get_backup_file_path(user_id, tool_id, backup_name)
        saved_content = self.__load(file_path)
        return saved_content

    def load_template(self, tool_id, tpl_name):
        file_path = self.__get_tpl_file_path(tool_id, tpl_name)
        saved_content = self.__load(file_path)
        return saved_content

    @staticmethod
    def __load(file_path):
        saved_content = {}
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                saved_content = pickle.load(f)
        return saved_content

    def delete_backup(self, user_id, tool_id, backup_name):
        file_path = self.__get_backup_file_path(user_id, tool_id, backup_name)
        self.__delete(file_path)

    def delete_template(self, tool_id, tpl_name):
        file_path = self.__get_tpl_file_path(tool_id, tpl_name)
        self.__delete(file_path)

    @staticmethod
    def __delete(file_path):
        if not os.path.isfile(file_path):
            raise ex.NotExistingFileError(file_path)
        os.remove(file_path)

    def get_available_backups_info(self, users_ids, tool_id):
        files_list = []
        if not users_ids or not tool_id:
            return files_list
        ext_len = len(FILE_EXTENSION)
        for user_id in users_ids:
            user_backup_dir_path = self.__get_user_backup_dir_path(user_id, tool_id)
            for entry in os.scandir(user_backup_dir_path):
                if not entry.name.startswith('.') and entry.is_file():
                    no_ext_name = entry.name[:-ext_len]
                    saved_content = self.load_backup(user_id, tool_id, no_ext_name)
                    if saved_content:
                        files_list.append(saved_content['info'])
        return files_list

    @staticmethod
    def __get_backup_file_path(user_id, tool_id, backup_name):
        file_name = backup_name + FILE_EXTENSION
        file_path = BACKUP_STORAGE_PATH + '/' + tool_id + '/' + user_id + '/' + file_name
        return file_path

    @staticmethod
    def __get_user_backup_dir_path(user_id, tool_id):
        user_backup_dir_path = BACKUP_STORAGE_PATH + '/' + tool_id + '/' + user_id
        return user_backup_dir_path

    @staticmethod
    def __get_tpl_file_path(tool_id, tpl_name):
        file_name = tpl_name + FILE_EXTENSION
        file_path = TPL_STORAGE_PATH + '/' + tool_id + '/' + file_name
        return file_path

    @staticmethod
    def __get_tpl_dir_path(tool_id):
        tpl_dir_path = TPL_STORAGE_PATH + '/' + tool_id
        return tpl_dir_path
