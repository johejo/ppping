DECIMAL_PLACES = 2


class SetLineError(RuntimeError):
    def __str__(self):
        return 'Could not set line'


class Line(object):
    def __init__(self, x, arg='', name='', space=1):
        self.arg = arg
        self.name = name
        self.host = str(None)
        self.address = str(None)
        self._x = x
        self.line = ''
        self.rtt = str(0)
        self.space = space

    def add_info(self, ping_result):
        self.host = ping_result.hostname
        self.address = ping_result.address
        self.rtt = str(round(ping_result.time, DECIMAL_PLACES))

    def add_char(self, char):
        self.line += char

    def reduce(self, result_len):
        if len(self.line) > result_len:
            self.line = self.line[1:]

    def x_pos(self):
        return self._x

    def y_pos(self):
        return len(self.line)

    def get_line(self, head_char, no_host, arg_len, name_len, host_len, address_len, rtt_len):

        arg = self.arg.ljust(arg_len + self.space)
        name = self.name.ljust(name_len + self.space)
        host = self.host.ljust(host_len + self.space)
        addr = self.address.ljust(address_len + self.space)
        rtt = self.rtt.ljust(rtt_len + self.space)

        if name_len and no_host:
            line = '{}{}{}{}{}{}'.format(head_char, arg, name, addr, rtt, self.line)

        elif name_len and (not no_host):
            line = '{}{}{}{}{}{}{}'.format(head_char, arg, name, host, addr, rtt, self.line)

        elif (not name_len) and no_host:
            line = '{}{}{}{}{}'.format(head_char, arg, addr, rtt, self.line)

        elif (not name_len) and (not no_host):
            line = '{}{}{}{}{}{}'.format(head_char, arg, host, addr, rtt, self.line)

        else:
            raise SetLineError

        return line
