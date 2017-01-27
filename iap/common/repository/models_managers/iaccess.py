from iap.common.repository.models_managers import layer_access as wha
from iap.common.repository.interface.service import (
    get_int_id_or_err as _get_id_or_err
)
from iap.common.repository import exceptions as ex


class IAccess:

    def __init__(self, **kwargs):
        try:
            self.ssn = kwargs['ssn'] if kwargs.get('ssn') is not None \
                else kwargs['ssn_factory']()
        except KeyError:
            raise Exception  # TODO update

    def get_permissions(self, tool_id, user_id):
        tool_id = _get_id_or_err(tool_id, 'tool_id')
        user_id = _get_id_or_err(user_id, 'user_id')

        tool = wha.get_tool_by_id(self.ssn, tool_id)
        user = wha.get_user_by_id(self.ssn, user_id)

        if tool is None:
            raise ex.NotExistsError('Tool', 'id', tool_id)
        if user is None:
            raise ex.NotExistsError('User', 'id', user_id)

        # default_perms = wha.get_perms_to_tool(ssn, tool)
        # wha.get_user_perms_to_tool(sess, tool, user),

        return {
            'permissions': wha.get_perms_to_tool(self.ssn, tool, user),
            'features': wha.get_user_features_to_tool(self.ssn, tool, user)
        }
