DECIMAL_PLACES = 2


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
        if len(self.line) >= result_len:
            self.line = self.line[1:]

    def x_pos(self):
        return self._x

    def y_pos(self):
        return len(self.line)

    def _ljust(self, target, length):
        return target.ljust(length + self.space)

    def get_line(self, head_char, no_host,
                 arg_len, name_len, host_len, address_len, rtt_len):

        arg = self._ljust(self.arg, arg_len)
        name = self._ljust(self.name, name_len)
        host = self._ljust(self.host, host_len)
        addr = self._ljust(self.address, address_len)
        rtt = self._ljust(self.rtt, rtt_len)

        if name_len and no_host:
            diff = ''.join([name])
        elif name_len and (not no_host):
            diff = ''.join([name, host])
        elif (not name_len) and no_host:
            diff = ''.join([])
        else:
            diff = ''.join([host])

        line = ''.join([head_char, arg, diff, addr, rtt, self.line])

        return line
