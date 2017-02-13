from pymodbus3.client.sync import ModbusTcpClient
from .target import FatekTarget


class Fatek(object):

    def __init__(self, address, port=502, logger=None):
        if not logger:
            import logging
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger = logger

        self.address = address
        self.client = ModbusTcpClient(address, port)

    def read(self, symbol):
        t = FatekTarget(self.client, symbol)
        return t.read()

    def write(self, symbol, value=True):
        t = FatekTarget(self.client, symbol)
        return t.write(value)

    def bulk_read(self, symbol, count, current_value=False):
        """
            current_value is for reading numeric values from T and C registers
        """
        t = FatekTarget(self.client, symbol, current_value)
        return t.read_all(int(count))
