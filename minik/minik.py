import webob
import webob.exc
import router


class Minik(object):
    """ WSGI application """
    def __init__(self):
        self.router = router.Router()

    def add_url(self, *args, **kwargs):
        self.router.add_url(*args, **kwargs)

    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        view, kwargs = self.router.get_view(request.path_info)
        if view:
            try:
                resp = view(request, **kwargs)
            except Exception, e:
                resp = webob.exc.HTTPInternalServerError(str(e))
            return resp(environ, start_response)
        return webob.exc.HTTPNotFound()(environ, start_response)
