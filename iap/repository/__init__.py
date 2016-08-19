"""
Describe package here.
"""

import pyramid

from iap.repository.interface import iaccess, imanage_access
from .db.warehouse import Warehouse

from ..repository.storage import *
from ..repository.interface.istorage import *

storage = Storage()
backup = IBackup(storage)
template = ITemplate(storage)
istorage = IStorage(backup, template)


def get_wh_interface():
    reg = pyramid.threadlocal.get_current_registry()
    wh = Warehouse(reg['dbsession_factory'])
    return wh
