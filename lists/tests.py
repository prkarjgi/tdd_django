from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolve_home_page(self):
        homepage = resolve('/')
        self.assertEqual(homepage.func, home_page)
