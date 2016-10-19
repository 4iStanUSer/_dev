# from pyramid.paster import get_app
# application = get_app('/var/www/IAP/production.ini', 'main')

from pyramid.paster import get_app, setup_logging
ini_path = '/var/www/IAP/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')

