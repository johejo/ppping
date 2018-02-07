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
    def __init__(self, args, timeout=1, rtt_scale=10, res_width=5, space=1, duration=sys.maxsize, interval=0.05,
                 config=None, no_host=False, mode=curses.A_BOLD):
        self.args = args
        self.res_width = res_width
        self.rtt_scale = rtt_scale
        self.space = space
        self.timeout = timeout
        self.duration = duration
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
            scale = '▁'
        elif rtt < self.rtt_scale * 2:
            scale = '▂'
        elif rtt < self.rtt_scale * 3:
            scale = '▃'
        elif rtt < self.rtt_scale * 4:
            scale = '▄'
        elif rtt < self.rtt_scale * 5:
            scale = '▅'
        elif rtt < self.rtt_scale * 6:
            scale = '▆'
        elif rtt < self.rtt_scale * 7:
            scale = '▇'
        else:
            scale = '█'

        return scale

    def _open_config(self):
        config = configparser.ConfigParser()
        config.read(self.config)
        d = dict(config.items(config.sections()[config.sections().index(HOSTS)]))
        self.names = list(d.keys())
        self.args = list(d.values())

    def _ljust(self, target, width):
        return target.ljust(width + self.space)

    def _display_title(self, info, arg_width, name_width, host_width, addr_width, rtt_width):
        version = '{} v{}'.format(__NAME__, __VERSION__)

        n_columns = sum((bool(arg_width), bool(name_width), bool(not self.no_host),
                         bool(addr_width), bool(rtt_width), bool(self.res_width)))

        width = max(sum((arg_width, name_width, host_width, addr_width, rtt_width,
                         self.res_width, n_columns * self.space)), len(info)) + len(version)

        self.stdscr.addstr(0, 0, version.rjust(width // 2), self.mode)
        self.stdscr.addstr(1, self.space - len(SPACE), info, self.mode)

        if name_width and self.no_host:
            string = '{}{}{}{}{}'.format(self._ljust(ARG, arg_width),
                                         self._ljust(NAME, name_width),
                                         self._ljust(ADDRESS, addr_width),
                                         self._ljust(RTT, rtt_width),
                                         RESULT.ljust(self.res_width))

        elif name_width and (not self.no_host):
            string = '{}{}{}{}{}{}'.format(self._ljust(ARG, arg_width),
                                           self._ljust(NAME, name_width),
                                           self._ljust(HOST, host_width),
                                           self._ljust(ADDRESS, addr_width),
                                           self._ljust(RTT, rtt_width),
                                           RESULT.ljust(self.res_width))

        elif (not name_width) and self.no_host:
            string = '{}{}{}{}'.format(self._ljust(ARG, arg_width),
                                       self._ljust(ADDRESS, addr_width),
                                       self._ljust(RTT, rtt_width),
                                       RESULT.ljust(self.res_width))

        elif (not name_width) and (not self.no_host):
            string = '{}{}{}{}{}'.format(self._ljust(ARG, arg_width),
                                         self._ljust(HOST, host_width),
                                         self._ljust(ADDRESS, addr_width),
                                         self._ljust(RTT, rtt_width),
                                         RESULT.ljust(self.res_width))

        else:
            raise DisplayTitleError

        self.stdscr.addstr(N_HEADERS + 1, self.space, string, self.mode)

        return True

    def _display_result(self, line, arg_width, name_width, host_width, addr_width, rtt_width):

        string = line.get_line(ARROW, self.no_host, arg_width, name_width, host_width, addr_width, rtt_width)
        self.stdscr.addstr(line.x_pos(), self.space - len(ARROW), string, self.mode)

        time.sleep(self.interval)
        self.stdscr.refresh()

        string = line.get_line(SPACE, self.no_host, arg_width, name_width, host_width, addr_width, rtt_width)
        self.stdscr.addstr(line.x_pos(), self.space - len(SPACE), string, self.mode)

        return True

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        lines = {a: Line(i + N_HEADERS + 2, a, name, self.space) for i, (a, name) in
                 enumerate(zip(self.args, self.names))}

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

            time.sleep(1 - self.interval * len(self.args))
