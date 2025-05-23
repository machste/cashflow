from pyramid.httpexceptions import HTTPFound


class View(object):

    def __init__(self, request):
        if request.identity is None:
            # Redirect to login page
            raise HTTPFound(location=request.route_url('login'))
        self.request = request
        self.user_id = request.identity.id
        self.dbsession = request.dbsession
        self.push_toast = self.request.session.push_toast