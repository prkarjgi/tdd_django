from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolve_home_page(self):
        homepage = resolve('/')
        self.assertEqual(homepage.func, home_page)

    def test_root_url_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')

        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
