from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_not_save_with_GET_request(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_after_POST_request(self):
        self.client.post('/', data={"new_item_text": "new item in to-do"})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "new item in to-do")

    def test_can_redirect_after_POST_request(self):
        response = self.client.post('/', data={"new_item_text": "other new item in to-do"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_template_shows_items(self):
        item1 = Item.objects.create(text="This is new item 1")
        item2 = Item.objects.create(text="This is new item 2")

        response = self.client.get('/')

        self.assertIn("This is new item 2", response.content.decode('utf-8'))
        self.assertIn("This is new item 1", response.content.decode('utf-8'))


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        item1 = Item.objects.create(text="This is item 1")
        item2 = Item.objects.create(text="This is item 2")

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        saved1 = items[0]
        saved2 = items[1]
        self.assertEqual(saved1.text, "This is item 1")
        self.assertEqual(saved2.text, "This is item 2")
