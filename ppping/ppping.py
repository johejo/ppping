import sys
import time
import curses
import subprocess
import socket
import configparser

from .line import Line
from .parser import PingResult

__VERSION__ = 'v0.1.5'
__NAME__ = 'PPPING'

COMMAND = 'ping'
COMMAND_OPT = '-c1'

RTT_DIGIT = 6
INTERVAL = 0.05
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
    def __init__(self, args, timeout=1, rtt_scale=10, res_width=5, space=1, duration=sys.maxsize, config=None,
                 no_host=False, mode=curses.A_BOLD):
        self.args = args
        self.res_width = res_width
        self.rtt_scale = rtt_scale
        self.space = space
        self.timeout = timeout
        self.duration = duration
        self.config = config
        self.names = ['' for _ in self.args]
        self.no_host = no_host
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
        d = dict(config.items(config.sections()[config.sections().index(HOSTS)]))
        self.names = list(d.keys())
        self.args = list(d.values())

    def _display_title(self, stdscr, info, arg_width, name_width, host_width, addr_width):
        version = '{} {}'.format(__NAME__, __VERSION__)

        n_columns = sum((bool(arg_width), bool(name_width), bool(not self.no_host),
                         bool(addr_width), bool(RTT_DIGIT), bool(self.res_width)))

        width = max(sum((arg_width, name_width, host_width, addr_width, RTT_DIGIT,
                         self.res_width, n_columns * self.space)), len(info)) + len(version)

        stdscr.addstr(0, 0, version.rjust(width // 2), self.mode)

        stdscr.addstr(1, 0, info, self.mode)

        if name_width and self.no_host:
            stdscr.addstr(N_HEADERS + 1, self.space, '{}{}{}{}{}'.format(ARG.ljust(arg_width + self.space),
                                                                         NAME.ljust(name_width + self.space),
                                                                         ADDRESS.ljust(addr_width + self.space),
                                                                         RTT.ljust(RTT_DIGIT + self.space),
                                                                         RESULT.ljust(self.res_width),
                                                                         ), self.mode)

        elif name_width and (not self.no_host):
            stdscr.addstr(N_HEADERS + 1, self.space, '{}{}{}{}{}{}'.format(ARG.ljust(arg_width + self.space),
                                                                           NAME.ljust(name_width + self.space),
                                                                           HOST.ljust(host_width + self.space),
                                                                           ADDRESS.ljust(addr_width + self.space),
                                                                           RTT.ljust(RTT_DIGIT + self.space),
                                                                           RESULT.ljust(self.res_width),
                                                                           ), self.mode)

        elif (not name_width) and self.no_host:
            stdscr.addstr(N_HEADERS + 1, self.space, '{}{}{}{}'.format(ARG.ljust(arg_width + self.space),
                                                                       ADDRESS.ljust(addr_width + self.space),
                                                                       RTT.ljust(RTT_DIGIT + self.space),
                                                                       RESULT.ljust(self.res_width),
                                                                       ), self.mode)

        elif (not name_width) and (not self.no_host):
            stdscr.addstr(N_HEADERS + 1, self.space, '{}{}{}{}{}'.format(ARG.ljust(arg_width + self.space),
                                                                         HOST.ljust(host_width + self.space),
                                                                         ADDRESS.ljust(addr_width + self.space),
                                                                         RTT.ljust(RTT_DIGIT + self.space),
                                                                         RESULT.ljust(self.res_width),
                                                                         ), self.mode)
        else:
            raise DisplayTitleError

        return True

    def _display_result(self, stdscr, line, arg_width, name_width, host_width, addr_width):

        stdscr.addstr(line.x_pos(), 0,
                      line.get_line(ARROW, self.no_host, arg_width, name_width,
                                    host_width, addr_width, RTT_DIGIT, self.space),
                      self.mode)

        time.sleep(INTERVAL)
        stdscr.refresh()

        stdscr.addstr(line.x_pos(), 0,
                      line.get_line(SPACE, self.no_host, arg_width, name_width,
                                    host_width, addr_width, RTT_DIGIT, self.space),
                      self.mode)

        return True

    def run(self, stdscr):
        begin = time.monotonic()

        stdscr.clear()

        lines = {a: Line(i + N_HEADERS + 2, arg=a, name=name) for i, (a, name) in enumerate(zip(self.args, self.names))}
        host_width = 0

        name_width = max([len(name) for name in self.names])

        hostname = socket.gethostname()

        info = '{}{}{}{}{}({})\n'.format(SPACE, FROM, SPACE, hostname, SPACE, socket.gethostbyname(hostname))

        while time.monotonic() - begin < self.duration:
            for a in self.args:
                line = lines[a]

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
                arg_width = max(max([len(v.arg) for v in lines.values()]), len(ARG))
                host_width = max(max([len(v.host) for v in lines.values()]), host_width, len(HOST))
                addr_width = max(max([len(v.address) for v in lines.values()]), len(ADDRESS))

                self._display_title(stdscr, info, arg_width, name_width, host_width, addr_width)

                self._display_result(stdscr, line, arg_width, name_width, host_width, addr_width)

            for line in lines.values():
                line.reduce(self.res_width)

            time.sleep(1 - INTERVAL * len(self.args))
