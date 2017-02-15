import os
import pickle
import datetime
from ...common import exceptions as ex
from os import getcwd, getcwdb

FILE_EXTENSION = '.pickle'
STORAGE_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

BACKUP_STORAGE_PATH = os.path.join(STORAGE_FOLDER_PATH, 'data_storage', 'for_backup_storage')
TPL_STORAGE_PATH = os.path.join(STORAGE_FOLDER_PATH, 'data_storage', 'for_tpl_storage')
CONFIG_STORAGE_PATH = os.path.join(STORAGE_FOLDER_PATH, 'data_storage', 'for_config_storage')


def load_backup(user_id, tool_id, project_id, backup_name):
    file_path = __get_backup_file_path(user_id, tool_id, project_id,
                                       backup_name)
    saved_content = __load(file_path)
    return saved_content['data']


def save_backup(user_id, tool_id, project_id, data_to_save, backup_name):
    folder = __get_user_backup_dir_path(user_id, tool_id, project_id)
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = __get_backup_file_path(user_id, tool_id, project_id,
                                       backup_name)
    file_info = {
        'name': backup_name,
        'user_id': user_id,
        'date': datetime.datetime.now()
    }
    __save(file_path, file_info, data_to_save)


def delete_backup(user_id, tool_id, project_id, backup_name):
    file_path = __get_backup_file_path(user_id, tool_id, project_id,
                                       backup_name)
    __delete(file_path)


def get_available_backups_info(users_ids, tool_id, project_id):
    files_list = []
    if not users_ids or not tool_id:
        return files_list
    ext_len = len(FILE_EXTENSION)
    for user_id in users_ids:
        user_backup_dir_path = __get_user_backup_dir_path(user_id, tool_id,
                                                          project_id)
        for entry in os.scandir(user_backup_dir_path):
            if not entry.name.startswith('.') and entry.is_file():
                no_ext_name = entry.name[:-ext_len]
                saved_content = load_backup(user_id, tool_id, project_id,
                                            no_ext_name)
                if saved_content:
                    files_list.append(saved_content['info'])
    return files_list


def load_template(tool_id, tpl_name):
    file_path = __get_tpl_file_path(tool_id, tpl_name)
    saved_content = __load(file_path)
    return saved_content


def save_template(tool_id, data_to_save, tpl_name='default_tpl'):
    if not os.path.exists(__get_tpl_dir_path(tool_id)):
        os.makedirs(__get_tpl_dir_path(tool_id))
    file_path = __get_tpl_file_path(tool_id, tpl_name)
    file_info = {
        'name': tpl_name,
        'date': datetime.datetime.now()
    }
    __save(file_path, file_info, data_to_save)


def delete_template(tool_id, tpl_name):
    file_path = __get_tpl_file_path(tool_id, tpl_name)
    __delete(file_path)


def __save(file_path, file_info, data_to_save):

    data_with_info = {
        'data': data_to_save,
        'info': file_info
    }
    with open(file_path, 'wb') as f:
        pickle.dump(data_with_info, f, pickle.HIGHEST_PROTOCOL)


def __load(file_path):
    saved_content = {}
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            saved_content = pickle.load(f)
    return saved_content


def __delete(file_path):
    if not os.path.isfile(file_path):
        raise ex.NotExistingFileError(file_path)
    os.remove(file_path)


def __get_backup_file_path(user_id, tool_id, project_id, backup_name):
    file_name = backup_name + FILE_EXTENSION
    file_path = os.path.join(BACKUP_STORAGE_PATH, str(user_id),
                             str(tool_id) + str(project_id), file_name)
    return file_path


def __get_user_backup_dir_path(user_id, tool_id, project_id):
    user_backup_dir_path = os.path.join(BACKUP_STORAGE_PATH,
                                        str(user_id),
                                        str(tool_id) + str(project_id))
    return user_backup_dir_path


def __get_tpl_file_path(tool_id, tpl_name):
    file_name = tpl_name + FILE_EXTENSION
    file_path = os.path.join(TPL_STORAGE_PATH, str(tool_id), file_name)
    return file_path


def __get_tpl_dir_path(tool_id):
    tpl_dir_path = os.path.join(TPL_STORAGE_PATH, str(tool_id))
    return tpl_dir_path
