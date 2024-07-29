from pyramid.view import (forbidden_view_config, notfound_view_config,
        exception_view_config)

from cashflow.errors import DatabaseError

@forbidden_view_config(renderer='cashflow:templates/errors/403.jinja2')
def forbidden_view(request):
    request.response.status = 403
    return {}

@notfound_view_config(renderer='cashflow:templates/errors/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}

@exception_view_config(DatabaseError,
        renderer='cashflow:templates/errors/500.jinja2')
def dberror_view(exc, request):
    request.response.status = 500
    return dict(topic='Datenbank Fehler', message=str(exc))