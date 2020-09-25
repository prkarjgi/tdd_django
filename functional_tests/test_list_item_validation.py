import os
import time
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest


MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_item(self):
        # User 1 goes to the home page
        # They accidentally hits enter without writing anything in the list

        # they sees that the page refreshes and is still on the home page
        # there is an error message saying the item cannot be left blank

        # They enter some values into the input box and hit enter
        # it adds to a new list

        # as a second test, they hit enter again without entering an item
        # it refreshes and returns the same error message

        self.fail("test has to be written")
