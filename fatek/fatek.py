try:
    from pymodbus3.client.sync import ModbusTcpClient
except ImportError:
    from pymodbus.client.sync import ModbusTcpClient

import logging

from .target import FatekTarget


class Fatek(object):

    def __init__(self, address, port=502, logger=None):
        if not logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger = logger

        self.address = address
        self.client = ModbusTcpClient(address, port)

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
