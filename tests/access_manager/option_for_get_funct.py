import pytest
from iap.common.security import build_permission_tree

def test_build_perm_tree():

    result = build_permission_tree(project_name = "JJOralCare", tool_id='forecast', user_id = 1)
    print("Result", result)