from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest


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
        self.fail('TO-DO: COMPLETE THE REST OF THIS TEST')

        # The user enters an item in their to-do list

        # They type the item in the text box and hit enter and the page updates and
        # adds a new item in their to-do list

        # The text box is still there and the user can enter another item. They add
        # another item and hit enter

        # There are now two new items on the to-do list

        # The user is concerned whether the site will remember their session if they
        # close the browser. They see a unique URL for them and there is text
        # explaining what it is.

        # They click on the URL and see that their to-do list is intact


if __name__ == "__main__":
    unittest.main()
