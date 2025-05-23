from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from cashflow.views import View
from cashflow.models.user import User
from cashflow.utils.form import Form
from cashflow.utils.db import get_user_roles
from cashflow.errors import DatabaseError


class Users(View):

    @view_config(route_name='user_add', permission="administrate",
            renderer='user_add.jinja2')
    def view(self):
        user_roles = get_user_roles(self.dbsession)
        form = Form('user_add', ['firstname', 'lastname', 'email', 'role',
                'password1', 'password2'])
        if 'form.submitted' in self.request.params:
            # Validate all fields
            for field in form.validate_each(self.request.params):
                if len(field.value) == 0:
                    field.err_msg = 'Dieses Feld darf nicht leer sein!'
                    continue
                if field.name == 'email':
                    if not field.is_email():
                        field.err_msg = 'Bitte gib eine gültige e-Mail Adresse ein!'
                        continue
                    # Check if a user with the same e-mail already exists
                    n_users = self.dbsession.query(func.count(User.id)).\
                            filter(User.email == field.value).scalar()
                    if n_users > 0:
                        field.err_msg = 'Diese e-Mail Adresse ist bereits registriert!'
                        continue
                if field.name == 'password2' \
                        and field.value != form.password1.value:
                    field.err_msg = 'Die Passwörter müssen übereinstimmen!'
            # If all fields are correct, save new user
            if form.is_valid():
                self.save_user(form)
                return HTTPSeeOther(self.request.route_url('users'))
        return dict(form=form, user_roles=user_roles)

    def save_user(self, form):
        user = User()
        user.firstname = form.firstname.value
        user.lastname = form.lastname.value
        user.email = form.email.value
        user.role = form.role.value
        user.set_password(form.password1.value)
        # Start nested transaction
        nested_transaction = self.dbsession.begin_nested()
        self.dbsession.add(user)
        try:
            nested_transaction.commit()
        except SQLAlchemyError as err:
            nested_transaction.rollback()
            raise DatabaseError(str(err))
