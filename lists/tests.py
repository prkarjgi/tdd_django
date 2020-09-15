from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.models import Item, List


# testing our home_page view functionality
class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


# tests on the item model
class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list1 = List()
        list1.save()

        item1 = Item.objects.create(text="This is item 1", item_list=list1)
        item2 = Item.objects.create(text="This is item 2", item_list=list1)

        lists = List.objects.first()
        self.assertEqual(list1, lists)

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        saved1 = items[0]
        saved2 = items[1]
        self.assertEqual(saved1.text, "This is item 1")
        self.assertEqual(saved1.item_list, list1)
        self.assertEqual(saved2.text, "This is item 2")
        self.assertEqual(saved2.item_list, list1)


# tests on the view view_list
class ListViewTest(TestCase):
    def test_list_view_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        item1 = Item.objects.create(text="This is new item 1", item_list=correct_list)
        item2 = Item.objects.create(text="This is new item 2", item_list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="This is item 1 of other list", item_list=other_list)
        Item.objects.create(text="This is item 2 of other list", item_list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, "This is new item 2")
        self.assertContains(response, "This is new item 1")
        self.assertNotContains(response, "This is item 1 of other list")
        self.assertNotContains(response, "This is item 2 of other list")


class NewListTest(TestCase):
    def test_can_save_after_POST_request(self):
        self.client.post(
            '/lists/new', data={"new_item_text": "new item in to-do"}
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "new item in to-do")

    def test_can_redirect_after_POST_request(self):
        response = self.client.post(
            '/lists/new', data={"new_item_text": "other new item in to-do"}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_.id}/")
