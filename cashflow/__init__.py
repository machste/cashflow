from pyramid.config import Configurator

from cashflow.security import SecurityPolicy
from cashflow.session import SessionFactory
from cashflow.utils.jinja2.filters import install_jinja2_filters
from cashflow.utils.forexrate.api import install_forexrate_api

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('cashflow:templates')
        config.action(None, install_jinja2_filters, args=(config, ))
        config.action(None, install_forexrate_api, args=(config, ))
        config.set_security_policy(
                SecurityPolicy(secret=settings['auth_cookie.secret']))
        config.set_session_factory(
                SessionFactory(secret=settings['session.secret']))
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
