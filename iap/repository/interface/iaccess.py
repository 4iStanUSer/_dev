from .. import exceptions as ex
from ..db import layer_access as wha
from .service import (
    get_int_id_or_err as _get_id_or_err,
    get_str_or_err as _get_str_or_err
)


class IAccess:

    def __init__(self):
        pass

    def get_permissions(self, ssn, tool_id, user_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        tool = wha.get_tool_by_id(ssn, tool_id)
        user = wha.get_user_by_id(ssn, user_id)

        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        # default_perms = wha.get_perms_to_tool(ssn, tool)
        # wha.get_user_perms_to_tool(sess, tool, user),

        return {
            'permissions': wha.get_perms_to_tool(ssn, tool, user),
            'features': wha.get_user_features_to_tool(ssn, tool, user)
        }
