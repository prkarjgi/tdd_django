from django.http import HttpRequest
from django.core.exceptions import ValidationError
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

    def test_cannot_save_empty_list_items(self):
        # The test here will run manual model validations but upon running
        # item.save(), it will save the faulty item to the Item model.
        # This error is not caught due to SQLite.
        # Try changing to Postgres and seeing if it persists
        list_ = List.objects.create()
        item = Item(item_list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
