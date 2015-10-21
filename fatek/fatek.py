from pymodbus.client.sync import ModbusTcpClient
from target import FatekTarget
import logging


class Fatek(object):
    """
        Base class which handle connection to PLC
    """
    def __init__(self, address, logger=None):
        if not logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger = logger

        self.address = address
        self.client = ModbusTcpClient(address)

    def read(self, symbol):
        target = FatekTarget(self.client, symbol)
        return target.read()

    def write(self, symbol, value=True):
        target = FatekTarget(self.client, symbol)
        return target.write(value)

    def bulk_read(self, symbol, count, current_value=False):
        """
            current_value is for reading numeric values from T and C registers
        """
        target = FatekTarget(self.client, symbol, current_value)
        return target.read_all(int(count))
