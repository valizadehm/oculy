from unittest import TestCase


class TestPlottingPlugin(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.figures = None

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_create_figure(self):
        if id in self.figures:
            self.assertRaises(KeyError)


    def test_destroy_figure(self):
        self.fail()

    def test_add_plot(self):
        self.fail()

    def test_get_resolver(self):
        self.fail()

    def test__populate_resolvers(self):
        self.fail()
