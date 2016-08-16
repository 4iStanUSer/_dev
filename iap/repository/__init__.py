"""
Describe package here.
"""

from iap.repository.interface import iaccess, imanage_access

from ..repository.storage import *
from ..repository.interface.istorage import *

storage = Storage()
backup = IBackup(storage)
template = ITemplate(storage)
istorage = IStorage(backup, template)
