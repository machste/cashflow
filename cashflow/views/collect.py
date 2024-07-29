from cmath import exp
from datetime import date
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy.exc import SQLAlchemyError

from cashflow.views import View
from cashflow.models.expenses import Expense
from cashflow.utils.form import Form
from cashflow.utils.db import (get_user_display_names, get_catetory_names,
        get_default_category, get_currency_codes, get_default_currency)
from cashflow.session import Toast
from cashflow.errors import DatabaseError


class Collect(View):

    @view_config(route_name='collect', renderer='collect.jinja2')
    def view(self):
        form = Form('collect', ['reporter', 'payer', 'date', 'amount',
                'currency', 'category', 'comment', 'private'])
        user_dnames = get_user_display_names(self.dbsession)
        cat_names = get_catetory_names(self.dbsession)
        curr_codes =  get_currency_codes(self.dbsession)
        # Check if form was submitted
        if 'form.submitted' in self.request.params:
            # Validate all fields
            for field in form.validate_each(self.request.params):
                if field.name == 'reporter':
                    # Always reset reporter to the logged in user
                    field.value = self.user_id
                    continue
                if field.name in ['payer', 'category', 'currency']:
                    try:
                        field.value = int(field.value)
                    except:
                        field.value = 0
                    if field.name == 'currency':
                        # Foreign currencies are not supported, yet.
                        if field.value != 1:
                            field.err_msg = 'Fremdwährungen sind nicht unterstützt!'
                    continue
                if field.name == 'amount':
                    try:
                        field.value = float(field.value)
                    except:
                        field.value = 0
                    if field.value <= 0:
                        field.err_msg = 'Betrag muss grösser als Null sein!'
                    continue
                if field.name == 'private':
                    field.value = field.value is not None
            # If all fields are correct, save new user
            if form.is_valid():
                self.save_expense(form)
                self.push_toast(f'Die Kosten von {curr_codes[form.currency.value]} {form.amount.value:.2f} wurden erfolgreich abgespeichert.',
                        title="Kosten erfasst!", type=Toast.Type.SUCCESS)
                return HTTPSeeOther(self.request.url)
        else:
            # Populate form with default values
            self.populate_form(form)
        return dict(user_dnames=user_dnames, cat_names=cat_names,
                curr_codes=curr_codes, form=form)

    def populate_form(self, form):
        form.reporter.value = self.user_id
        form.payer.value = self.user_id
        form.date.value = date.today().isoformat()
        form.amount.value = 0
        form.currency.value = get_default_currency(self.dbsession, self.user_id)
        form.category.value = get_default_category(self.dbsession, self.user_id)

    def reset_form(self, form):
        form.reset()
        self.populate_form(form)

    def save_expense(self, form):
        expense = Expense()
        expense.reporter_id = self.user_id
        expense.payer_id = form.payer.value
        expense.date = date.fromisoformat(form.date.value)
        expense.amount = form.amount.value
        expense.category_id = form.category.value
        expense.comment = form.comment.value
        expense.private = form.private.value
        # Start nested transaction
        nested_transaction = self.dbsession.begin_nested()
        self.dbsession.add(expense)
        try:
            nested_transaction.commit()
        except SQLAlchemyError as err:
            nested_transaction.rollback()
            raise DatabaseError(str(err))
