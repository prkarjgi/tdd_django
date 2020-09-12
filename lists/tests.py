from django.test import TestCase


# Create your tests here.
class SmokeTest(TestCase):
    # expected failure testcase
    def test_sample(self):
        self.assertEqual(1 + 1, 3)
