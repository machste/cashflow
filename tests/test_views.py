from cashflow import models
from cashflow.views.collect import Collect
from cashflow.views.errors import notfound_view


def test_my_view_failure(app_request):
    info = Collect(app_request)
    assert info.status_int == 500

def test_my_view_success(app_request, dbsession):
    model = models.User(name='one', value=55)
    dbsession.add(model)
    dbsession.flush()

    info = Collect(app_request)
    assert app_request.response.status_int == 200
    assert info['one'].name == 'one'
    assert info['project'] == 'cashflow'

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
