from errors import InvalidTargetError

class Symbol(object):
    register, number = None, None

    def __init__(self, symbol, current_value=True):
        self.current_value = current_value

        try:
            self.register = symbol[:1]
            self.number = int(symbol[1:])
        except:
            raise InvalidTargetError("Not allowed coil/register number")

        self.__verify_number()
        self.offset = self.__calculate_offset()

    def __str__(self):
        return "%s%s" % (self.register, self.number)

    def __calculate_offset(self):
        """
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

        target = self.register
        number = self.number
        current_value = self.current_value

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
        if target == 'C' and current_value == True and number >= 200:
            number %= 200
            offset = 9700 + 2*(number)
        elif target == 'R' and number >= 5000:
            number = 0
            offset = 5000

        return number + offset

    def __verify_number(self):
        number = self.number
        target = self.register

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
