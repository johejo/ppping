import sys
import time
import curses
import subprocess
import socket

from .line import Line
from .parser import PingResult

__VERSION__ = '0.1.1'

RTT_DIGIT = 5
INTERVAL = 0.05


class PPPing(object):
    def __init__(self, args, timeout=5, rtt_scale=10, result_len=5, space=2, duration=sys.maxsize, mode=curses.A_BOLD):
        self.args = args
        self.result_len = result_len
        self.rtt_scale = rtt_scale
        self.space = space
        self.timeout = timeout
        self.duration = duration
        self.mode = mode

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

    def run(self, stdscr):
        begin = time.monotonic()

        stdscr.clear()
        nheaders = 4

        lines = {h: Line(i + nheaders, arg=h) for i, h in enumerate(self.args)}
        host_len = 0

        hostname = socket.gethostname()

        info = 'From: {} ({})\n'.format(hostname, socket.gethostbyname(hostname))

        while time.monotonic() - begin < self.duration:
            for h in self.args:
                line = lines[h]
                try:
                    out = subprocess.run(['ping', h, '-c1'], check=True, stdout=subprocess.PIPE, timeout=self.timeout) \
                        .stdout.decode()
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    c = 'X'
                else:
                    p = PingResult(out)
                    c = self._scale_char(p.time)
                    line.add_info(p)

                line.add_char(c)
                arg_len = max([len(v.arg) for v in lines.values()])
                host_len = max(max([len(v.host) for v in lines.values()]), host_len)
                address_len = max([len(v.address) for v in lines.values()])

                _, x = stdscr.getmaxyx()
                version = 'PPPING v{}'.format(__VERSION__)
                stdscr.addstr(0, 0, version.rjust(int((x + len(version)) / 2 - 1)), self.mode)

                stdscr.addstr(1, self.space, info, self.mode)

                stdscr.addstr(nheaders - 1, self.space, '{}{}{}{}{}'.format('args'.ljust(arg_len + self.space),
                                                                        'host'.ljust(host_len + self.space),
                                                                        'address'.ljust(address_len + self.space),
                                                                        'rtt'.ljust(RTT_DIGIT + self.space),
                                                                        'result'.ljust(self.result_len),
                                                                        ), self.mode)

                stdscr.addstr(line.x_pos(), self.space - 1,
                              '>' + line.get_line(arg_len, host_len, address_len, RTT_DIGIT, self.space),
                              self.mode)

                time.sleep(INTERVAL)
                stdscr.refresh()

                stdscr.addstr(line.x_pos(), self.space - 1,
                              ' ' + line.get_line(arg_len, host_len, address_len, RTT_DIGIT, self.space),
                              self.mode)

            for line in lines.values():
                line.reduce(self.result_len)
            time.sleep(1 - INTERVAL)
