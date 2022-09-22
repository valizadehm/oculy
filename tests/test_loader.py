from unittest import TestCase


class TestDataKeyError(TestCase):
    pass


class TestBaseLoader(TestCase):
    def test_load_data(self):
        self.assertRaises(NotImplementedError)

    def test_determine_content(self):
        pass

    def test_clear(self):
        self.assertRaises(NotImplementedError)

