from .errors import InvalidTargetError

from .symbol import Symbol


class FatekTarget(object):
    """
        Manipulate on PLC objects

        accessible read, write, read_all function,
        which are picked according to desred Symbol
    """

    client = None  # Fatek instance
    symbol = None  # Symbol

    # function handlers
    read = None
    write = None

    # MODBUS Application Protocol Specification V1.1b
    # http://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf
    # - page 12
    quantity_limit_of_coils = 2000
    # - page 15
    quantity_limit_of_registers = 125

    def __init__(self, client, symbol_str, current_value=False):
        self.client = client
        self.symbol = Symbol(symbol_str, current_value=current_value)

        self._assign_functions()

    def read_all(self, count):
        """ Read all available stuff from PLC """
        number = self.symbol.offset

        if self.symbol.is_coil():
            # params: (start, number of readed bits)
            if count > self.quantity_limit_of_coils:
                raise InvalidTargetError()
            return self.client.read_coils(number, count).bits
        else:
            # params: (start, number of readed bits)
            if count > self.quantity_limit_of_registers:
                raise InvalidTargetError()
            return self.client.read_holding_registers(number, count).registers

    def _assign_functions(self):
        if self.symbol.is_coil():
            self.read = self._read_coil
            self.write = self._write_coil
        else:
            self.read = self._read_holding_r
            self.write = self._write_holding_r

    def _read_coil(self):
        # params: (start coil, number of readed bits)
        return self.client.read_coils(self.symbol.offset, 1).bits[0]

    def _write_coil(self, value):
        return self.client.write_coil(self.symbol.offset, value)

    def _read_holding_r(self):
        # params: (start , number of readed bytes)
        return self.client.read_holding_registers(self.symbol.offset, 1).registers[0]

    def _write_holding_r(self, value):
        return self.client.write_register(self.symbol.offset, value)
