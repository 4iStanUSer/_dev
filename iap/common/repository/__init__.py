"""
Describe package here.
"""

import pyramid

from iap.common.repository.models_managers.admin_manager import IManageAccess as __IManAcc
from iap.common.repository.models_managers.iaccess import IAccess as __IAccess
from iap.common.repository.models_managers.warehouse import Warehouse as __Warehouse


def get_wh_interface():
    reg = pyramid.threadlocal.get_current_registry()
    wh = __Warehouse(reg['dbsession_factory'])
    return wh


def get_access_interface(ssn=None):
    if ssn is None:
        reg = pyramid.threadlocal.get_current_registry()
        iaccess = __IAccess(ssn_factory=reg['dbsession_factory'])
    else:
        iaccess = __IAccess(ssn=ssn)
    return iaccess


def get_manage_access_interface(ssn=None):
    if ssn is None:
        reg = pyramid.threadlocal.get_current_registry()
        imanager_access = __IManAcc(ssn_factory=reg['dbsession_factory'])
    else:
        imanager_access = __IManAcc(ssn=ssn)
    return imanager_access
