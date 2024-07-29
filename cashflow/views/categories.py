from pyramid.view import view_config

from cashflow.views import View


class Categories(View):

    @view_config(route_name='categories', renderer='categories.jinja2')
    def view(self):
        return {}
