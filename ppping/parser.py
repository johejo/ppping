class PingParserError(RuntimeError):
    def __str__(self):
        return 'Could not parse ping message.'


class PingResult(object):
    def __init__(self, ping_message):
        self.raw = ping_message
        if type(self.raw) is not str:
            self.raw = self.raw.decode()

        try:
            sp = self.raw.split('\n')[1].split(' ')

            if len(sp) == 9:
                self.hostname = sp[-6]
                self.address = sp[-5][1:-2]
            elif len(sp) == 8:
                self.hostname = sp[-5][:-1]
                self.address = self.hostname
            else:
                raise PingParserError(self.raw)

            self.icmp_seq = int(sp[-4].split('=')[-1])
            self.ttl = int(sp[-3].split('=')[-1])
            self.time = float(sp[-2].split('=')[-1])

        except ValueError:
            raise PingParserError

    def __str__(self):
        return 'host={}, address={}, icmp_sec={}, ttl={}, time={}'.\
            format(self.hostname, self.address, self.icmp_seq, self.ttl, self.time)
