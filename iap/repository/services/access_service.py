from IAP.repository.warehouse import exceptions as ex

class AccessService():
    def __init__(self, warh_common):
        self.warh_common = warh_common

    def get_user_permissions(self, user):
        if user is None:
            raise ex.EmptyInputsError('user')
        output = {}
        for role in user.roles:
            for perm in role.feature_permissions:
                feature = self.warh_common.get_feature(id=perm.feature_id)
                feature_name = feature.name
                tool = self.warh_common.get_tool(id=feature.tool_id)
                tool_name = tool.name
                if tool_name not in output:
                    output[tool.name] = {}
                if feature_name not in output[tool.name]:
                     output[tool.name][feature_name] = []
                output[tool.name][feature_name].append(perm.name)
        return output