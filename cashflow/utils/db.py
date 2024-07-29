from cashflow.models.user import User
from cashflow.models.categories import Category
from cashflow.models.currencies import Currency

def get_user_roles(dbsession):
    # Currently this is hardcoded
    return { 'basic': 'Benutzer', 'admin': 'Administrator' }

def get_user_display_names(dbsession, limit=50):
    display_names = {}
    users = dbsession.query(User).limit(limit).all()
    for user in users:
        display_names[user.id] = user.display_name
    return display_names

def get_default_category(dbsession, user_id=None):
    # Currently this is hardcoded
    return 1

def get_default_currency(dbsession, user_id=None):
    # Currently this is hardcoded
    return 1

def get_catetory_names(dbsession, limit=50):
    category_names = {}
    for id, name in dbsession.query(Category.id, Category.name).limit(limit):
        category_names[id] = name
    return category_names

def get_currency_codes(dbsession, limit=50):
    currency_codes = {}
    for id, code in dbsession.query(Currency.id, Currency.code).limit(limit):
        currency_codes[id] = code
    return currency_codes