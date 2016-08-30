"""
Describe package here.
"""

import pyramid

from .db.warehouse import Warehouse

from ..repository.storage import *
from ..repository.interface.istorage import *
from ..repository.interface.iaccess import IAccess as __IAccess
from ..repository.interface.imanage_access import  IManageAccess as __IManAcc

storage = Storage()
backup = IBackup(storage)
template = ITemplate(storage)
istorage = IStorage(backup, template)
iaccess = __IAccess()
imanage_access = __IManAcc(iaccess, istorage)


def get_wh_interface():
    reg = pyramid.threadlocal.get_current_registry()
    wh = Warehouse(reg['dbsession_factory'])
    return wh
