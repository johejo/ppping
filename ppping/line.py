DECIMAL_PLACES = 2


class Line(object):
    def __init__(self, nstage, arg='', name=''):
        self.arg = arg
        self.name = name
        self.host = ''
        self.address = ''
        self._x = nstage
        self.line = ''
        self.rtt = '0'
        self.snt = '0'

    def add_info(self, ping_result):
        self.host = ping_result.hostname
        self.address = ping_result.address
        self.rtt = str(round(ping_result.time, 2))

    def add_char(self, char):
        self.line += char

    def reduce(self, result_len):
        if len(self.line) > result_len:
            self.line = self.line[1:]

    def x_pos(self):
        return self._x

    def y_pos(self):
        return len(self.line)

    def get_line(self, arg_len, name_len, host_len, address_len, rtt_digit, space):

        if name_len:
            line = '{}{}{}{}{}{}'.format(self.arg.ljust(arg_len + space, ' '),
                                         self.name.ljust(name_len + space, ' '),
                                         self.host.ljust(host_len + space, ' '),
                                         self.address.ljust(address_len + space, ' '),
                                         self.rtt.ljust(rtt_digit + space, ' '),
                                         self.line)
        else:
            line = '{}{}{}{}{}'.format(self.arg.ljust(arg_len + space, ' '),
                                       self.host.ljust(host_len + space, ' '),
                                       self.address.ljust(address_len + space, ' '),
                                       self.rtt.ljust(rtt_digit + space, ' '),
                                       self.line)

        return line
