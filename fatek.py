from pymodbus.client.sync import ModbusTcpClient
import logging

from target import FatekTarget

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Fatek(object):
    def __init__(self, address='192.168.13.250'):
        self.address = address
        self.client = ModbusTcpClient(address)

    def read(self, symbol):
        t = FatekTarget(self.client, symbol)
        return t.read()

    def write(self, symbol, value=True):
        t = FatekTarget(self.client, symbol)
        return t.write(value)

