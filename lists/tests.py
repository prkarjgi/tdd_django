from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_POST_request(self):
        response = self.client.post('/', data={"new_item_text": "new item in to-do"})
        # print(response.content.decode('utf-8'))
        self.assertIn("new item in to-do", response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = "This is item 1"
        item1.save()

        item2 = Item()
        item2.text = "This is item 2"
        item2.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        saved1 = items[0]
        saved2 = items[1]
        self.assertEqual(saved1.text, "This is item 1")
        self.assertEqual(saved2.text, "This is item 2")
