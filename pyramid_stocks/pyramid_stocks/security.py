import os
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


class MyRoot:
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view')
        (Allow, Authenticated, 'secret')
    ]


def includeme(config):
    auth_secret = os.environ.get('AUTH_SECRET', 'issasecret')
    authz_policy = ACLAuthorizationPolicy()
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512',
    )

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('secret')

    session_secret = os.environ.get('SESSION_SECRET', 'issasecrettoo')
    session_factory = SignedCookieSessionFactory(session_secret)

    config.set_session_factory(session_factory)
    config.set_default_csrf(require_csrf=True)
