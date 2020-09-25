from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.models import Item, List


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
