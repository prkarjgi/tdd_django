from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.models import Item


# testing our home_page view functionality
class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


# tests on the item model
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


# tests on the view view_list
class ListViewTest(TestCase):
    def test_list_view_uses_list_template(self):
        response = self.client.get('/lists/list-for-user/')
        self.assertTemplateUsed(response, 'list.html')

    def test_show_all_list_items(self):
        item1 = Item.objects.create(text="This is new item 1")
        item2 = Item.objects.create(text="This is new item 2")

        response = self.client.get('/lists/list-for-user/')

        self.assertContains(response, "This is new item 2")
        self.assertContains(response, "This is new item 1")


class NewListTest(TestCase):
    def test_can_save_after_POST_request(self):
        self.client.post('/lists/new', data={"new_item_text": "new item in to-do"})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "new item in to-do")

    def test_can_redirect_after_POST_request(self):
        response = self.client.post('/lists/new', data={"new_item_text": "other new item in to-do"})
        self.assertRedirects(response, "/lists/list-for-user/")
