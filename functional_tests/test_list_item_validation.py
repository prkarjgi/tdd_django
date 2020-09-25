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
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys(Keys.ENTER)

        # they sees that the page refreshes and is still on the home page
        # there is an error message saying the item cannot be left blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You cannot add an empty list item"
            )
        )

        # They enter some values into the input box and hit enter
        # it adds to a new list
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Placeholder values for item")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_new_item_in_todo("1: Placeholder values for item")

        # as a second test, they hit enter again without entering an item
        # it refreshes and returns the same error message
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You cannot add an empty list item"
            )
        )

        # They add a new item and then check if the items are there in the list
        self.browser.find_element_by_id("id_new_item").send_keys("dummy 2")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        self.wait_for_new_item_in_todo("2: dummy 2")
        self.wait_for_new_item_in_todo("1: Placeholder values for item")
