"""
Describe package here.
"""

import pyramid

from .db.warehouse import Warehouse

from ..repository.storage import *
from ..repository.interface.istorage import *

from ..repository.interface.iaccess import IAccess as __IAccess
iaccess = __IAccess()

from ..repository.interface.imanage_access import \
    IManageAccess as __IManageAccess
imanage_access = __IManageAccess()

storage = Storage()
backup = IBackup(storage)
template = ITemplate(storage)
istorage = IStorage(backup, template)


def get_wh_interface():
    reg = pyramid.threadlocal.get_current_registry()
    wh = Warehouse(reg['dbsession_factory'])
    return wh
