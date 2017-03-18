from unittest.case import TestCase
from unittest.mock import MagicMock

from fatek.target import FatekTarget


class TestTarget(TestCase):

    def setUp(self):
        self.client = MagicMock()

    def test_Y0(self):
        FatekTarget(self.client, 'Y33').read()
        self.client.read_coils.assert_called_once_with(33, 1)

    def test_X10(self):
        FatekTarget(self.client, 'X10').read()
        self.client.read_coils.assert_called_once_with(1010, 1)

    def test_M0(self):
        FatekTarget(self.client, 'M0').read()
        self.client.read_coils.assert_called_once_with(2000, 1)

    def test_R333(self):
        FatekTarget(self.client, 'R333').read()
        self.client.read_holding_registers.assert_called_once_with(333, 1)

    def test_T255c(self):
        FatekTarget(self.client, 'T255', current_value=False).read()
        self.client.read_coils.assert_called_once_with(9255, 1)

    def test_T255r(self):
        FatekTarget(self.client, 'T255', current_value=True).read()
        self.client.read_holding_registers.assert_called_once_with(9255, 1)
