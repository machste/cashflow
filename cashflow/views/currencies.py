import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy.exc import SQLAlchemyError

from cashflow.views import View
from cashflow.models import Currency
from cashflow.utils.toast import Toast
from cashflow.utils.forexrate.api import Api
from cashflow.errors import DatabaseError

_log = logging.getLogger(__name__)

class Currencies(View):

    @view_config(route_name='currencies', renderer='currencies.jinja2')
    def view(self):
        currencies = self.dbsession.query(Currency).all()
        return dict(currencies=currencies)

    @view_config(route_name='currencies_update', permission="administrate")
    def update_view(self):
        if not self.update_currencies():
            self.push_toast(f'Die Devisenkurse konnten nicht aktualisiert werden!',
                        title="Fehler!", type=Toast.Type.DANGER)
        return HTTPSeeOther(self.request.route_url('currencies'))

    def update_currencies(self):
        # Get all currencies
        currencies = self.dbsession.query(Currency).all()
        # Update all rates
        try:
            self.request.forexrate_api.update_rates(currencies)
        except Api.Error as err:
            _log.error("Unable to update currencies: {err.msg}")
            return False
        # Save the updated currencies
        nested_transaction = self.dbsession.begin_nested()
        self.dbsession.add_all(currencies)
        try:
            nested_transaction.commit()
        except SQLAlchemyError as err:
            nested_transaction.rollback()
            raise DatabaseError(str(err))
        return True