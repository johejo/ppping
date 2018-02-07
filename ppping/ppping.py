import sys
import time
import curses
import subprocess
import socket
import configparser

from .line import Line
from .parser import PingResult

__VERSION__ = '0.1.6'
__NAME__ = 'PPPING'

COMMAND = 'ping'
COMMAND_OPT = '-c1'

N_HEADERS = 2

FAILED = 'X'
ARROW = '>'
SPACE = ' '

ARG = 'arg'
NAME = 'name'
HOST = 'host'
ADDRESS = 'address'
RTT = 'rtt'
RESULT = 'result'

HOSTS = 'Hosts'
FROM = 'From:'


class DisplayTitleError(RuntimeError):
    def __str__(self):
        return 'Could not set display title.'


class PPPing(object):
    def __init__(self, args, *, timeout=1, rtt_scale=10, res_width=5, space=1, duration=sys.maxsize, interval=0.8,
                 step=0.05, config=None, no_host=False, mode=curses.A_BOLD):
        self.args = args
        self.res_width = res_width
        self.rtt_scale = rtt_scale
        self.space = space
        self.timeout = timeout
        self.duration = duration
        self.step = step
        self.config = config
        self.names = ['' for _ in self.args]
        self.no_host = no_host
        self.interval = interval
        self.mode = mode
        self.stdscr = None

        if self.config is not None:
            self._open_config()

    def _scale_char(self, rtt):
        if rtt < self.rtt_scale:
            char = '▁'
        elif rtt < self.rtt_scale * 2:
            char = '▂'
        elif rtt < self.rtt_scale * 3:
            char = '▃'
        elif rtt < self.rtt_scale * 4:
            char = '▄'
        elif rtt < self.rtt_scale * 5:
            char = '▅'
        elif rtt < self.rtt_scale * 6:
            char = '▆'
        elif rtt < self.rtt_scale * 7:
            char = '▇'
        else:
            char = '█'

        return char

    def _open_config(self):
        config = configparser.ConfigParser()
        config.read(self.config)
        d = dict(config.items(config.sections()[config.sections().index(HOSTS)]))
        self.names = list(d.keys())
        self.args = list(d.values())

    def _ljust(self, target, width):
        return target.ljust(width + self.space)

    def _calc_width(self, info, arg_width, name_width, host_width, addr_width, rtt_width):
        ncolums = sum((bool(arg_width), bool(name_width), bool(not self.no_host),
                       bool(addr_width), bool(rtt_width), bool(self.res_width)))

        s = sum((arg_width, name_width, host_width, addr_width, rtt_width, self.res_width, ncolums * self.space))

        return max(s, len(info))

    def _display_title(self, info, arg_width, name_width, host_width, addr_width, rtt_width):
        version = '{} v{}'.format(__NAME__, __VERSION__)

        width = self._calc_width(info, arg_width, name_width, host_width, addr_width, rtt_width) + len(version)

        self.stdscr.addstr(0, 0, version.rjust(width // 2), self.mode)
        self.stdscr.addstr(1, self.space - len(SPACE), info, self.mode)

        arg = self._ljust(ARG, arg_width)
        name = self._ljust(NAME, name_width)
        host = self._ljust(HOST, host_width)
        addr = self._ljust(ADDRESS, addr_width)
        rtt = self._ljust(RTT, rtt_width)
        res = RESULT.ljust(self.res_width)

        if name_width and self.no_host:
            string = '{}{}{}{}{}'.format(arg, name, addr, rtt, res)

        elif name_width and (not self.no_host):
            string = '{}{}{}{}{}{}'.format(arg, name, host, addr, rtt, res)

        elif (not name_width) and self.no_host:
            string = '{}{}{}{}'.format(arg, addr, rtt, res)

        elif (not name_width) and (not self.no_host):
            string = '{}{}{}{}{}'.format(arg, host, addr, rtt, res)

        else:
            raise DisplayTitleError

        self.stdscr.addstr(N_HEADERS + 1, self.space, string, self.mode)

        return True

    def _display_result(self, line, arg_width, name_width, host_width, addr_width, rtt_width):

        string = line.get_line(ARROW, self.no_host, arg_width, name_width, host_width, addr_width, rtt_width)
        self.stdscr.addstr(line.x_pos(), self.space - len(ARROW), string, self.mode)

        time.sleep(self.step)

        self.stdscr.refresh()
        self.stdscr.addstr(line.x_pos(), self.space - len(SPACE), string.replace(ARROW, SPACE), self.mode)

        return True

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        lines = {a: Line(i + N_HEADERS + 2, a, n, self.space) for i, (a, n) in enumerate(zip(self.args, self.names))}

        hostname = socket.gethostname()
        info = '{}{}{}{}{}({})\n'.format(SPACE, FROM, SPACE, hostname, SPACE, socket.gethostbyname(hostname))

        arg_width = len(ARG)
        host_width = len(HOST)
        addr_width = len(ADDRESS)
        rtt_width = len(RTT)
        name_width = max([len(name) for name in self.names])

        begin = time.monotonic()

        while time.monotonic() - begin < self.duration:
            for a, line in lines.items():
                try:
                    out = subprocess.run([COMMAND, a, COMMAND_OPT], check=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL, timeout=self.timeout).stdout.decode()
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    c = FAILED
                else:
                    p = PingResult(out)
                    c = self._scale_char(p.time)
                    line.add_info(p)

                line.add_char(c)

                arg_width = max(max([len(v.arg) for v in lines.values()]), arg_width)
                host_width = max(max([len(v.host) for v in lines.values()]), host_width)
                addr_width = max(max([len(v.address) for v in lines.values()]), addr_width)
                rtt_width = max(max([len(v.rtt) for v in lines.values()]), rtt_width)

                self._display_title(info, arg_width, name_width, host_width, addr_width, rtt_width)
                self._display_result(line, arg_width, name_width, host_width, addr_width, rtt_width)

            for line in lines.values():
                line.reduce(self.res_width)

            time.sleep(self.interval)
