from pyramid.view import view_config

from cashflow.views import View
from cashflow.models.categories import Category


class Categories(View):

    @view_config(route_name='categories', renderer='categories.jinja2')
    def view(self):
        categories = self.dbsession.query(Category).all()
        return dict(categories=categories)
