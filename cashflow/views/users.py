from pyramid.view import view_config

from cashflow.views import View
from cashflow.models.user import User


class Users(View):

    @view_config(route_name='users', permission="administrate",
            renderer='users.jinja2')
    def view(self):
        users = self.dbsession.query(User).all()
        return dict(users=users)
