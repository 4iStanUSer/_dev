from ...repository import exceptions as ex
from ..warehouse import wh_access as wha


def _get_int_id_or_err(value, name):
    try:
        integer = int(value)
        if integer < 1:
            raise ex.WrongArgEx(name, value)
        return integer
    except TypeError:
        raise ex.EmptyInputsError(name)
    except ValueError:
        raise ex.WrongArgEx(name, value)


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

    return {
        'permissions': wha.get_user_perms_to_tool(sess, tool, user),
        'features': wha.get_user_features_to_tool(sess, tool, user)
    }


# def get_features(req, tool_id, user_id):
#     tool_id = _get_int_id_or_err(tool_id, 'tool_id')
#     user_id = _get_int_id_or_err(user_id, 'user_id')
#
#     sess = req.dbsession
#     tool = wha.get_tool(sess, id=tool_id)
#     user = wha.get_user(sess, id=user_id)
#
#     if tool is None:
#         raise ex.NotExistsError('Tool', 'id', tool_id)
#     if user is None:
#         raise ex.NotExistsError('User', 'id', user_id)
#
#     return wha.get_user_features_to_tool(sess, tool, user)
