import os
import time
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.getenv('STAGING_SERVER', None)
        if staging_server is not None:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        self.browser.quit()

    # helper method
    def wait_for_new_item_in_todo(self, item_text):
        start_time = time.time()
        while True:
            try:
                to_do_items = self.browser.find_element_by_id("id_to_do_list")
                rows = to_do_items.find_elements_by_tag_name("tr")
                self.assertIn(item_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
