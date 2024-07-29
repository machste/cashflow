from pyramid.view import view_config

from cashflow.views import View


class Settings(View):

    @view_config(route_name='settings', renderer='settings.jinja2')
    def view(self):
        return dict()

