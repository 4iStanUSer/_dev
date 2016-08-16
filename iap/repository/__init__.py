"""
Describe package here.
"""
from .services import access_service, adm_access_service

from ..repository.storage import *
from ..repository.interface.istorage import *

storage = Storage()
backup = IBackup(storage)
template = ITemplate(storage)
istorage = IStorage(backup, template)
