import os
import pickle
import datetime
from . import exceptions as ex

FILE_EXTENTION = '.pickle'
STORAGE_PATH = 'for_storage'


class BackupStorage:

    def save(self, user_id, tool_name, data_to_save, backup_name='default'):
        if not os.path.exists(self.__get_user_dir_path(user_id, tool_name)):
            os.makedirs(self.__get_user_dir_path(user_id, tool_name))
        file_path = self.__get_file_path(user_id, tool_name, backup_name)
        data_with_info = {
            'data': data_to_save,
            'info': {
                'name': backup_name,
                'user_id': user_id,
                'date': datetime.datetime.now()
                }
            }
        with open(file_path, 'wb') as f:
            pickle.dump(data_with_info, f, pickle.HIGHEST_PROTOCOL)

    def load(self, user_id, tool_name, backup_name):
        file_path = self.__get_file_path(user_id, tool_name, backup_name)
        saved_content = {}
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                saved_content = pickle.load(f)
        return saved_content

    def delete(self, user_id, tool_name, backup_name):
        file_path = self.__get_file_path(user_id, tool_name, backup_name)
        if not os.path.isfile(file_path):
            raise ex.NotExistingFileError(file_path)
        os.remove(file_path)

    def get_available_info(self, users_ids, tool_name):
        files_list = []
        if not users_ids or not tool_name:
            return files_list
        ext_len = len(FILE_EXTENTION)
        for user_id in users_ids:
            user_dir_path = self.__get_user_dir_path(user_id, tool_name)
            for entry in os.scandir(user_dir_path):
                if not entry.name.startswith('.') and entry.is_file():
                    no_ext_name = entry.name[:-ext_len]
                    saved_content = self.load(user_id, tool_name, no_ext_name)
                    if saved_content:
                        files_list.append(saved_content['info'])
        return files_list

    @staticmethod
    def __get_file_path(user_id, tool_name, backup_name):
        file_name = backup_name + FILE_EXTENTION
        file_path = STORAGE_PATH + '/' + tool_name + '/' + user_id + '/' + file_name
        return file_path

    @staticmethod
    def __get_user_dir_path(user_id, tool_name):
        user_dir_path = STORAGE_PATH + '/' + tool_name + '/' + user_id
        return user_dir_path
