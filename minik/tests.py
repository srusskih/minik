import unittest
import router
import minik
import webob


def test_view(request, slug=None):
    return webob.Response("slug: \"{0}\"".format(slug))


class TestLoadViewFunc(unittest.TestCase):
    def test_func(self):
        self.assert_(router.load_view('tests.test_view'))
        self.assertRaises(
            AttributeError,
            router.load_view, 'tests.test_view_notexists'
        )
        self.assertRaises(
            ImportError,
            router.load_view, 'tests_doesnotexist.test_view_notexists'
        )


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = router.Router()

    def test_add_url(self):
        self.assertEqual(len(self.router.routs), 0)
        self.router.add_url('^/page/(?P<slug>[-\w]+)/$', 'tests.test_view')
        self.assertEqual(len(self.router.routs), 1)
        self.assertIsInstance(self.router.routs[0][1], basestring)

    def test_get_view(self):
        self.router.add_url('^/page/(?P<slug>[-\w]+)/$', 'tests.test_view')

        # get almost match
        view, kwargs = self.router.get_view('/page/super-article-about-webob')
        self.assertIsNone(view)
        self.assertIsNone(kwargs)

        # get success match
        view, kwargs = self.router.get_view('/page/super-article-about-webob/')
        self.assertIsNotNone(view)
        self.assertIsNotNone(kwargs)

    def test_unchanged_routs(self):
        """ After success functions finding view function and
            default values should not be changed in routs list
        """
        self.router.add_url('^/page/(?P<slug>[-\w]+)/$', 'tests.test_view')
        view, kwargs = self.router.get_view('/page/super-article-about-webob/')

        _, func_path, defaults = self.router.routs[0]
        self.assertEqual(defaults, {})
        self.assertEqual(func_path, 'tests.test_view')


class TestMinik(unittest.TestCase):
    def setUp(self):
        self.app = minik.Minik()
        self.app.add_url('^/page/(?P<slug>[-\w]+)/$', 'tests.test_view')

    def test_200(self):
        request = webob.Request.blank('http://localhost/page/test/')
        response = request.get_response(self.app)
        self.assertEqual(response.status_int, 200)
        self.assertIn('slug: "test"', response.text)

    def test_404(self):
        request = webob.Request.blank('http://localhost/blog/')
        response = request.get_response(self.app)
        self.assertEqual(response.status_int, 404)

    def _test_500(self):
        request = webob.Request.blank('http://localhost/blog/')
        response = request.get_response(self.app)
        self.assertEqual(response.status_int, 404)


if __name__ == '__main__':
    unittest.main()
