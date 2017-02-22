from unittest.case import TestCase

from fatek.fatek import Fatek


class testFatek(TestCase):

    def test_ok(self):
        Fatek('localhost')
