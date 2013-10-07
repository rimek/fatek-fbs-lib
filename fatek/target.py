from errors import InvalidTargetError

class FatekTarget(object):
    client = None # pymodbus client
    target, number = None, None # str, int
    cv = False # bool - current value - (coil/register access)
    read, write = None, None # access functions

    def __init__(self, client, symbol_str, cv=False):
        self.client = client
        self.cv = cv

        self._read_symbol(symbol_str)

        self._verify_number()
        self._choose_functions()
        self._calculate_offset()

    def _read_symbol(self, symbol):

        self.target = symbol[0]
        self.number = int(symbol[1:])

    def _choose_functions(self):
        target = self.target
        cv = self.cv

        if target in ['Y', 'X', 'M', 'S'] or (cv == False and target in ['T', 'C']):
            self.read = self._read_coil
            self.write = self._write_coil
        elif target in ['R', 'D'] or (cv == True and target in ['T', 'C']):
            self.read = self._read_holding_r
            self.write = self._write_holding_r

    def _calculate_offset(self):
        """
            # coils:
            Y(0-255) : 0 - 255
            X(0-255) : 1000 - 1255
            M(0-2001): 2000 - 4001
            S(0-999) : 6000 - 6999
            T(0-255) : 9000 - 9255 (cv=False)
            C(0-255) : 9500 - 9755 (cv=False)

            # registers
            R(0-4167)    : 0    - 4167
            R(5000-5998) : 5000 - 5998 (holding or ror)
            D(0-2998)    : 6000 - 8998
            T(0-255)     : 9000 - 9255 (cv = True)
            C(0-199)     : 9500 - 9699 (16bit, cv=True)
            C(200-255)   : 9700 - 9811 (32bit, cv=True) double offset
        """

        target = self.target
        number = self.number
        cv = self.cv

        offset_dict = {
            'Y': 0,
            'X': 1000,
            'M': 2000,
            'S': 6000,
            'T': 9000,
            'R': 0,
            'D': 6000,
            'C': 9500
        }

        offset = offset_dict[target]
        if target == 'C' and cv == True and number >= 200:
            number %= 200
            offset = 9700 + 2*(number)
        elif target == 'R' and number >= 5000:
            number = 0
            offset = 5000

        self.number = number + offset

    def _verify_number(self):
        number = self.number
        target = self.target

        allowed_numbers = {
            'Y': (0,256),
            'X': (0,256),
            'M': (0,2002),
            'S': (0,1000),
            'T': (0,256),
            'D': (0,2999),
            'C': (0,256)
        }
        allowed_r_numbers = ((0, 4168), (5000, 5999))

        if target != 'R':
            result = number in xrange(*allowed_numbers[target])
        else:
            result = any([number in xrange(*numbers) for numbers in allowed_r_numbers])

        if not result:
            raise InvalidTargetError("Not allowed coil/register number")

    def _read_coil(self):
        return self.client.read_coils(self.number, 1).bits[0] # (start coil, number of readed bits)
    def _write_coil(self, value):
        return self.client.write_coil(self.number, value)

    def _read_holding_r(self):
        return self.client.read_holding_registers(self.number, 1).registers[0] # (start , number of readed bytes)
    def _write_holding_r(self, value):
        return self.client.write_register(self.number, value)

