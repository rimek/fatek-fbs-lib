from unittest.case import TestCase

from fatek.errors import InvalidTargetError
from fatek.symbol import Symbol


class TestSymbol(TestCase):

    def test_Y0(self):
        s = Symbol('Y33')
        self.assertEqual(s.offset, 33)
        self.assertTrue(s.is_coil())

    def test_X10(self):
        s = Symbol('X10')
        self.assertEqual(s.offset, 1010)
        self.assertTrue(s.is_coil())

    def test_M0(self):
        s = Symbol('M0')
        self.assertEqual(s.offset, 2000)
        self.assertTrue(s.is_coil())

    def test_S5(self):
        s = Symbol('S5')
        self.assertEqual(s.offset, 6005)
        self.assertTrue(s.is_coil())

    def test_R333(self):
        s = Symbol('R333')
        self.assertEqual(s.offset, 333)
        self.assertFalse(s.is_coil())

    def test_R5234_is_5000(self):
        s = Symbol('R5234')
        self.assertEqual(s.offset, 5000)
        self.assertFalse(s.is_coil())

    def test_D593(self):
        s = Symbol('D593')
        self.assertEqual(s.offset, 6593)
        self.assertFalse(s.is_coil())

    def test_T255c(self):
        s = Symbol('T255', current_value=False)
        self.assertEqual(s.offset, 9255)
        self.assertTrue(s.is_coil())

    def test_T255r(self):
        s = Symbol('T255', current_value=True)
        self.assertEqual(s.offset, 9255)
        self.assertFalse(s.is_coil())

    def test_C255c(self):
        s = Symbol('C255', current_value=False)
        self.assertEqual(s.offset, 9755)
        self.assertTrue(s.is_coil())

    def test_C255r(self):
        s = Symbol('C255', current_value=True)
        self.assertEqual(s.offset, 9810)
        self.assertFalse(s.is_coil())

    def test_not_found(self):
        with self.assertRaises(InvalidTargetError):
            Symbol('Z33')

    def test_X_not_found(self):
        with self.assertRaises(InvalidTargetError):
            Symbol('X9999')
