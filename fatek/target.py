from symbol import Symbol

class FatekTarget(object):
    client, symbol = None, None
    current_value = False # bool - current value - (coil/register access)
    read, write = None, None # access functions

    def __init__(self, client, symbol_str, current_value=False):
        self.client = client
        self.current_value = current_value
        self.symbol = Symbol(symbol_str)
        self.__assign_functions()

    def __assign_functions(self):
        target = self.symbol.register

        if target in ['Y', 'X', 'M', 'S']:
            self.read = self._read_coil
            self.write = self._write_coil
        elif target in ['R', 'D', 'C', 'T']:
            self.read = self._read_holding_r
            self.write = self._write_holding_r

    def _read_coil(self):
        return self.client.read_coils(self.symbol.offset, 1).bits[0] # (start coil, number of readed bits)

    def _write_coil(self, value):
        return self.client.write_coil(self.symbol.offset, value)

    def _read_holding_r(self):
        return self.client.read_holding_registers(self.symbol.offset, 1).registers[0] # (start , number of readed bytes)

    def _write_holding_r(self, value):
        return self.client.write_register(self.symbol.offset, value)

    def read_all(self, count):
        target = self.symbol.register
        number = self.symbol.offset
        current_value = self.current_value

        if target in ['Y', 'X', 'M', 'S'] or (current_value == False and target in ['T', 'C']):
            return self.client.read_coils(number, count).bits # (start coil, number of readed bits)

        elif target in ['R', 'D'] or (current_value == True and target in ['T', 'C']):
            return self.client.read_holding_registers(number, count).registers # (start, number of readed bits)
