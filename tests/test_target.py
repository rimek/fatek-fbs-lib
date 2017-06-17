from unittest.case import TestCase
from mock import MagicMock

from fatek.errors import InvalidTargetError
from fatek.target import FatekTarget


class TestTarget(TestCase):

    def setUp(self):
        self.client = MagicMock()

    def test_Y0(self):
        FatekTarget(self.client, 'Y33').read()
        self.client.read_coils.assert_called_once_with(33, 1)

    def test_X10(self):
        FatekTarget(self.client, 'X10').write(5)
        self.client.write_coil.assert_called_once_with(1010, 5)

    def test_M0(self):
        FatekTarget(self.client, 'M0').read()
        self.client.read_coils.assert_called_once_with(2000, 1)

    def test_R333(self):
        FatekTarget(self.client, 'R333').read()
        self.client.read_holding_registers.assert_called_once_with(333, 1)

    def test_D333(self):
        FatekTarget(self.client, 'D333').write(593)
        self.client.write_register.assert_called_once_with(6333, 593)

    def test_T255c(self):
        FatekTarget(self.client, 'T255', current_value=False).read()
        self.client.read_coils.assert_called_once_with(9255, 1)

    def test_T255r(self):
        FatekTarget(self.client, 'T255', current_value=True).read()
        self.client.read_holding_registers.assert_called_once_with(9255, 1)

    def test_M300_readall(self):
        FatekTarget(self.client, 'M300').read_all(50)
        self.client.read_coils.assert_called_once_with(2300, 50)

    def test_R300_readall(self):
        FatekTarget(self.client, 'R300').read_all(55)
        self.client.read_holding_registers.assert_called_once_with(300, 55)

    def test_coil_range_2000(self):
        with self.assertRaises(InvalidTargetError):
            FatekTarget(self.client, 'M0').read_all(2001)

    def test_register_range_125(self):
        with self.assertRaises(InvalidTargetError):
            FatekTarget(self.client, 'R300').read_all(155)
