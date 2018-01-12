import sys
import time
import curses
import subprocess
import socket
import configparser

from .line import Line
from .parser import PingResult

__VERSION__ = '0.1.4'

RTT_DIGIT = 6
INTERVAL = 0.05
NHEADERS = 3


class PPPing(object):
    def __init__(self, args, timeout=1, rtt_scale=10, result_len=5, space=1, duration=sys.maxsize, config=None,
                 mode=curses.A_BOLD):
        self.args = args
        self.result_len = result_len
        self.rtt_scale = rtt_scale
        self.space = space
        self.timeout = timeout
        self.duration = duration
        self.config = config
        self.names = ['' for _ in self.args]
        self.mode = mode

        if self.config is not None:
            self._open_config()

    def _scale_char(self, rtt):
        if rtt < self.rtt_scale:
            return '▁'
        elif rtt < self.rtt_scale * 2:
            return '▂'
        elif rtt < self.rtt_scale * 3:
            return '▃'
        elif rtt < self.rtt_scale * 4:
            return '▄'
        elif rtt < self.rtt_scale * 5:
            return '▅'
        elif rtt < self.rtt_scale * 6:
            return '▆'
        elif rtt < self.rtt_scale * 7:
            return '▇'
        else:
            return '█'

    def _open_config(self):
        config = configparser.ConfigParser()
        config.read(self.config)
        d = dict(config.items(config.sections()[config.sections().index('Hosts')]))
        self.names = list(d.keys())
        self.args = list(d.values())

    def run(self, stdscr):
        begin = time.monotonic()

        stdscr.clear()

        lines = {a: Line(i + NHEADERS + 1, arg=a, name=name) for i, (a, name) in enumerate(zip(self.args, self.names))}
        host_len = 0

        name_len = max([len(name) for name in self.names])

        hostname = socket.gethostname()

        info = 'From: {} ({})\n'.format(hostname, socket.gethostbyname(hostname))

        while time.monotonic() - begin < self.duration:
            for h in self.args:
                line = lines[h]
                try:
                    out = subprocess.run(['ping', h, '-c1'], check=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL, timeout=self.timeout).stdout.decode()
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    sys.stderr.flush()
                    sys.stdout.flush()
                    c = 'X'
                else:
                    p = PingResult(out)
                    c = self._scale_char(p.time)
                    line.add_info(p)

                line.add_char(c)
                arg_len = max([len(v.arg) for v in lines.values()])
                host_len = max(max([len(v.host) for v in lines.values()]), host_len)
                address_len = max([len(v.address) for v in lines.values()])

                version = 'PPPING v{}'.format(__VERSION__)
                n = (arg_len + host_len + address_len + RTT_DIGIT + self.result_len + 5 * self.space)
                stdscr.addstr(0, 0, version.rjust((n + len(version)) // 2), self.mode)

                stdscr.addstr(1, self.space, info, self.mode)

                if not name_len:
                    stdscr.addstr(NHEADERS, self.space, '{}{}{}{}{}'.format('args'.ljust(arg_len + self.space),
                                                                            'host'.ljust(host_len + self.space),
                                                                            'address'.ljust(address_len + self.space),
                                                                            'rtt'.ljust(RTT_DIGIT + self.space),
                                                                            'result'.ljust(self.result_len),
                                                                            ), self.mode)
                else:
                    stdscr.addstr(NHEADERS, self.space, '{}{}{}{}{}{}'.format('args'.ljust(arg_len + self.space),
                                                                              'name'.ljust(name_len + self.space),
                                                                              'host'.ljust(host_len + self.space),
                                                                              'address'.ljust(address_len + self.space),
                                                                              'rtt'.ljust(RTT_DIGIT + self.space),
                                                                              'result'.ljust(self.result_len),
                                                                              ), self.mode)

                stdscr.addstr(line.x_pos(), self.space - 1,
                              '>' + line.get_line(arg_len, name_len, host_len, address_len, RTT_DIGIT, self.space),
                              self.mode)

                time.sleep(INTERVAL)
                stdscr.refresh()

                stdscr.addstr(line.x_pos(), self.space - 1,
                              ' ' + line.get_line(arg_len, name_len, host_len, address_len, RTT_DIGIT, self.space),
                              self.mode)

            for line in lines.values():
                line.reduce(self.result_len)

            time.sleep(1 - INTERVAL)
