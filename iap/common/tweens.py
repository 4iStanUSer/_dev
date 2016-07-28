import time
#import logging
from pyramid.settings import asbool

#log = logging.getLogger(__name__)

def timing_tween_factory(handler, registry):
    # TODO checking conf
    #if asbool(registry.settings.get('do_timing')):
    def timing_tween(request):
        start = time.time()
        response = None # ????
        try:
            response = handler(request)
        finally:
            if response is not None:
                end = time.time()
                response.headerlist.append(('X-Timing', str(end - start)))
            #log.debug('The request took %s seconds' %
            #          (end - start))
        return response
    return timing_tween

    return handler