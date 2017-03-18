from .symbol import Symbol


class FatekTarget(object):
    """
        Manipulate on PLC objects

        accessible read, write, read_all function,
        which are picked according to desred Symbol
    """

    client = None  # Fatek instance
    symbol = None  # Symbol

    # TODO figure out whats that
    current_value = False  # whether is coil or register (?)

    # function handlers
    read = None
    write = None

    def __init__(self, client, symbol_str, current_value=False):
        self.client = client
        self.symbol = Symbol(symbol_str, current_value=current_value)

        self._assign_functions()

    def read_all(self, count):
        """ Read all available stuff from PLC """
        number = self.symbol.offset

        if self.symbol.isCoil():
            # params: (start, number of readed bits)
            return self.client.read_coils(number, count).bits
        else:
            # params: (start, number of readed bits)
            return self.client.read_holding_registers(number, count).registers

    def _assign_functions(self):
        if self.symbol.isCoil():
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
