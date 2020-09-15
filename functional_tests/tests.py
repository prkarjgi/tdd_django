from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

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

    def test_can_start_list_for_one_user(self):
        # User goes to application site
        self.browser.get(self.live_server_url)

        # User sees To-Do in the title of the page and sees To-Do lists in the header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The user sees an input box telling them to enter a new item to the list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            "Enter a new item",
            inputbox.get_attribute("placeholder")
        )

        # The user enters an item in their to-do list
        inputbox.send_keys("Buy 3 milk bags")
        # They type the item in the text box and hit enter and the page updates and
        # adds a new item in their to-do list
        inputbox.send_keys(Keys.ENTER)

        # They see the new item added to the to-do list
        self.wait_for_new_item_in_todo("1: Buy 3 milk bags")

        # The text box is still there and the user can enter another item. They add
        # another item and hit enter
        inputbox = self.browser.find_element_by_id("id_new_item")
        # print(self.browser.current_url)
        inputbox.send_keys("Buy some butter")
        inputbox.send_keys(Keys.ENTER)

        # There are now two new items on the to-do list
        self.wait_for_new_item_in_todo("1: Buy 3 milk bags")
        self.wait_for_new_item_in_todo("2: Buy some butter")

    def test_multiple_users_can_start_new_list(self):
        # User 1 connects to the application using their browser
        self.browser.get(self.live_server_url)

        # They add an item and see it has been added
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy a new car")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_new_item_in_todo("1: Buy a new car")

        # User 1 sees their list has unique URL
        user1_url = self.browser.current_url
        self.assertRegex(user1_url, "/lists/.+")

        # User 1 closes their browser
        self.browser.quit()

        # A new user, User 2 opens their browser and goes to the application.
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        # User 2 sees that none of User 1's items are there
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy a new car", page_text)
        self.assertNotIn("Random values", page_text)

        # User 2 adds an item to the list and sees that is has been added
        # to their list
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy a loaf of bread")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_new_item_in_todo("1: Buy a loaf of bread")

        # they see that they have a unique URL created for their lists
        # this unique URL is not the same as User 1's URL
        user2_url = self.browser.current_url
        self.assertRegex(user2_url, "/lists/")
        self.assertNotEqual(user2_url, user1_url)

        # there is no trace of User 1's activity
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("1: Buy a new car", page_text)
        self.assertIn("1: Buy a loaf of bread", page_text)

        # User 2 and User 1 are satisfied
