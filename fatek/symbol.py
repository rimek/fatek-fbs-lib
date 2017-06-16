from .errors import InvalidTargetError


class Symbol(object):
    """
        Representation of PLC value

        # coils:
        Y(0-255) : 0 - 255
        X(0-255) : 1000 - 1255
        M(0-2001): 2000 - 4001
        S(0-999) : 6000 - 6999
        T(0-255) : 9000 - 9255 (current_value=False)
        C(0-255) : 9500 - 9755 (current_value=False)

        # registers
        R(0-4167)    : 0    - 4167
        R(5000-5998) : 5000 - 5998 (holding or ror)
        D(0-2998)    : 6000 - 8998
        T(0-255)     : 9000 - 9255 (current_value = True)
        C(0-199)     : 9500 - 9699 (16bit, current_value=True)
        C(200-255)   : 9700 - 9811 (32bit, current_value=True) double offset
    """

    register = None
    number = None

    allowed_numbers = {
        'Y': (0, 256),
        'X': (0, 256),

        'M': (0, 2002),
        'S': (0, 1000),
        'T': (0, 256),
        'D': (0, 2999),
        'C': (0, 256)
    }

    allowed_r_numbers = ((0, 4168), (5000, 5999))

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

    def __init__(self, symbol, current_value=True):
        self.current_value = current_value

        self.register = symbol[:1]
        self.number = int(symbol[1:])

        self._verify_type()
        self._verify_number()

        self.offset = self.__calculate_offset()

    def __str__(self):
        return "%s%s" % (self.register, self.number)

    def __unicode__(self):
        return str(self)

    def __calculate_offset(self):
        register = self.register
        number = self.number
        current_value = self.current_value

        offset = self.offset_dict[register]
        if register == 'C' and current_value and number >= 200:
            number %= 200
            number += number
            offset = 9700
        elif register == 'R' and number >= 5000:
            number = 0
            offset = 5000

        return number + offset

    def _verify_type(self):
        if not self.register or self.register not in self.offset_dict.keys():
            raise InvalidTargetError("Not allowed coil/register type")

    def _verify_number(self):
        if self.register != 'R':
            result = self.number in range(*self.allowed_numbers[self.register])
        else:
            result = any([self.number in range(*numbers)
                          for numbers in self.allowed_r_numbers])

        if not result:
            raise InvalidTargetError("Not allowed coil/register number")

    def is_coil(self):
        if self.register in ['Y', 'X', 'M', 'S']:
            return True
        elif self.register in ['R', 'D']:
            return False
        elif self.register in ['T', 'C'] and self.current_value:
            return False
        elif self.register in ['T', 'C'] and not self.current_value:
            return True
