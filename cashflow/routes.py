from importlib import metadata
from pyramid.traversal import DefaultRootFactory
from pyramid.authorization import Allow


class CashflowRoot(DefaultRootFactory):

    APP_VERSION = metadata.version('cashflow')

    def __acl__(self):
        return [
            (Allow, 'role:admin', 'administrate')
        ]

def includeme(config):
    config.set_root_factory(CashflowRoot)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('collect', '/collect')
    config.add_route('overview', '/overview')
    config.add_route('users', '/users')
    config.add_route('user_add', '/user/add')
    config.add_route('categories', '/categories')
    config.add_route('currencies', '/currencies')
    config.add_route('currencies_update', '/currencies/update')
    config.add_route('myaccount', '/myaccount')
    config.add_route('settings', '/settings')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
