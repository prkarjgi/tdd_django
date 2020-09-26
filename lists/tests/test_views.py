from django.http import HttpRequest
from django.urls import resolve
from django.utils.html import escape
from django.test import TestCase
from lists.models import Item, List


# testing our home_page view functionality
class HomePageTest(TestCase):
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # def test_home_page_redirects_after_POST_request(self):
    #     response = self.client.post(
    #         path='/',
    #         data={
    #             "new_text_item": "placeholder text"
    #         }
    #     )
    #     print(response.context['request'])
    #     self.assertEqual(response.status_code, 302)


# tests on the view view_list
class ListViewTest(TestCase):
    def test_list_view_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        item1 = Item.objects.create(
            text="This is new item 1", item_list=correct_list
        )
        item2 = Item.objects.create(
            text="This is new item 2", item_list=correct_list
        )

        other_list = List.objects.create()
        Item.objects.create(
            text="This is item 1 of other list", item_list=other_list
        )
        Item.objects.create(
            text="This is item 2 of other list", item_list=other_list
        )

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, "This is new item 2")
        self.assertContains(response, "This is new item 1")
        self.assertNotContains(response, "This is item 1 of other list")
        self.assertNotContains(response, "This is item 2 of other list")

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'], correct_list)
        self.assertNotEqual(response.context['list'], other_list)


class NewListTest(TestCase):
    def test_can_save_after_POST_request(self):
        self.client.post(
            '/lists/new', data={"new_item_text": "new item in to-do"}
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, "new item in to-do")

    def test_can_redirect_after_POST_request(self):
        response = self.client.post(
            path='/lists/new',
            data={"new_item_text": "other new item in to-do"}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_.id}/")

    def test_validation_errors_sent_to_home_page_template(self):
        response = self.client.post(
            path="/lists/new", data={"new_item_text": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You cannot add an empty list item")
        self.assertContains(response, expected_error)

    def test_empty_item_not_added_to_list(self):
        response = self.client.post(
            path="/lists/new", data={"new_item_text": ""}
        )
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={
                "new_item_text": "placeholder text for item"
            }
        )

        new_item = Item.objects.first()
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, "placeholder text for item")
        self.assertNotEqual(new_item.text, "New text for item")
        self.assertEqual(new_item.item_list, correct_list)
        self.assertNotEqual(new_item.item_list, other_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={
                "new_item_text": "new placeholder text"
            }
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
