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
        self.current_value = current_value
        self.symbol = Symbol(symbol_str)

        self._assign_functions()

    def read_all(self, count):
        """ Read all available stuff from PLC """
        target = self.symbol.register
        number = self.symbol.offset

        if target in ['Y', 'X', 'M', 'S'] or (not self.current_value and target in ['T', 'C']):
            # params: (start, number of readed bits)
            return self.client.read_coils(number, count).bits

        elif target in ['R', 'D'] or (self.current_value and target in ['T', 'C']):
            # params: (start, number of readed bits)
            return self.client.read_holding_registers(number, count).registers

    def _assign_functions(self):
        target = self.symbol.register

        if target in ['Y', 'X', 'M', 'S']:
            self.read = self._read_coil
            self.write = self._write_coil
        elif target in ['R', 'D', 'C', 'T']:
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
