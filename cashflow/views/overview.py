from pyramid.view import view_config
from sqlalchemy import desc

from cashflow.views import View
from cashflow.models.expenses import Expense


class Overview(View):

    @view_config(route_name='overview', renderer='overview.jinja2')
    def view(self):
        recent_expenses = self.dbsession.query(Expense).\
                order_by(desc(Expense.date)).\
                limit(30).all()
        return dict(recent_expenses=recent_expenses)