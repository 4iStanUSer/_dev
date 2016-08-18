"""
Describe package here.
"""
from iap.repository.interface.iaccess import IAccess as __IAccess
from iap.repository.interface.imanage_access import \
    IManageAccess as __IManageAccess

iaccess = __IAccess()
imanage_access = __IManageAccess()
