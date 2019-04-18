from unittest import TestCase
import pixab

class TestPixab(TestCase):
    def test_randomize_query(self):
        queries = ["bird","flower","cat",
                   "dog", "computer", "abstract", "magic"]
        self.assertIn(pixab.randomize_query(), queries)
