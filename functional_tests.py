from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_new_visitor_remember_list(self):
        # User goes to application site
        try:
            self.browser.get("http://localhost:8000")
        except WebDriverException as e:
            print(e)
            self.fail('Connection to server failed')

        # User sees To-Do in the title of the page and sees To-Do lists in the header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)

        # The user sees an input box telling them to enter a new item to the list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            "enter a new item",
            inputbox.get_attribute("placeholder")
        )

        # The user enters an item in their to-do list
        inputbox.send_keys("Buy 3 milk bags")
        # They type the item in the text box and hit enter and the page updates and
        # adds a new item in their to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # They see the new item added to the to-do list
        to_do_items = self.browser.find_element_by_id("id_to_do_list")
        rows = to_do_items.find_elements_by_tag_name("tr")
        self.assertIn(
            "Buy 3 milk bags",
            rows
        )

        # The text box is still there and the user can enter another item. They add
        # another item and hit enter
        self.fail("ADD TESTS FOR SUBSEQUENT ENTRIES AND REMEMBERING THE USER ACTIVITY")

        # There are now two new items on the to-do list

        # The user is concerned whether the site will remember their session if they
        # close the browser. They see a unique URL for them and there is text
        # explaining what it is.

        # They click on the URL and see that their to-do list is intact


if __name__ == "__main__":
    unittest.main()
