from . import service
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Authenticated
from pyramid.security import Allow
my_session_factory = SignedCookieSessionFactory('itsaseekreet')

class Root:
    __acl__ = [
        (Allow, Authenticated, ('read',)),
    ]

    def __init__(self, request):
        pass

def validate_the_token():
    pass


def get_user(request):
    return 111
    #user_id = request.unauthenticated_userid
    #if user_id is not None:
    #    #user = request.dbsession.query(User).get(user_id)
    #    user = service.get_user_by_id(user_id)
    #    return user




def includeme(config):
    settings = config.get_settings()
    config.set_jwt_authentication_policy('secret', http_header='X-Token')
    config.set_session_factory(my_session_factory)
    config.add_request_method(get_user, 'user', reify=True)