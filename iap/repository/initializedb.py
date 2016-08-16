import os
import sys
import transaction

from pyramid.paster import (get_appsettings, setup_logging)

from pyramid.scripts.common import parse_vars

from .db.meta import Base
from .db import (get_engine, get_session_factory, get_tm_session)
from .db.warehouse import Entity


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings, prefix='sqlalchemy.')

    session_factory = get_session_factory(engine)

    with transaction.manager:
        ssn = get_tm_session(session_factory, transaction.manager)
        # TODO remove procedure of removing all rows
        # Drop all tables
        Base.metadata.drop_all(engine)
        # Create all tables
        Base.metadata.create_all(engine)
        # Add root to entities tree.
        root = Entity(name='root')
        ssn.add(root)
        transaction.manager.commit()
