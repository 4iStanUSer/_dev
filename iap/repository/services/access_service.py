from ...repository import exceptions as ex
from ..warehouse import wh_access as wha
from . import get_int_id_or_err as _get_int_id_or_err


def get_permissions(req, tool_id, user_id):
    tool_id = _get_int_id_or_err(tool_id, 'tool_id')
    user_id = _get_int_id_or_err(user_id, 'user_id')

    sess = req.dbsession
    tool = wha.get_tool_by_id(sess, tool_id)
    user = wha.get_user_by_id(sess, user_id)

    if tool is None:
        raise ex.NotExistsError('Tool', 'id', tool_id)
    if user is None:
        raise ex.NotExistsError('User', 'id', user_id)

    default_perms = wha.get_default_perms_to_tool(sess, tool)

    return {
        'permissions': wha.get_user_perms_to_tool(sess, tool, user),
        'features': wha.get_user_features_to_tool(sess, tool, user)
    }

