from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_POST_request(self):
        response = self.client.post('/', data={"new_item_text": "new item in to-do"})
        # print(response.content.decode('utf-8'))
        self.assertIn("new item in to-do", response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'home.html')
