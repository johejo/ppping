import configparser
import curses
import os
import shutil
import socket
import subprocess
import sys
import time

from .__version__ import __version__, __title__
from .line import Line
from .parser import PingResult

N_HEADERS = 3

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
GLOBAL = 'Global:'

PING_CMD = 'ping'
PING4_CMD = 'ping4'
PING6_CMD = 'ping6'
PING_OPT = '-c1'
IFCONFIG_URL = 'https://ifconfig.io/ip'
CURL_CMD = 'curl'
OPT_IPV4 = '-4'
OPT_IPV6 = '-6'


def get_ip_info(opt):
    return subprocess.run([CURL_CMD, IFCONFIG_URL, opt],
                          check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, timeout=2,
                          ).stdout.decode().strip()


class PPPing(object):
    def __init__(self, args, *, timeout=1, rtt_scale=10, res_width=5, space=1,
                 duration=sys.maxsize, interval=0.8, step=0.05, closed=False,
                 config=None, no_host=False, only_ipv4=False, only_ipv6=False,
                 mode=curses.A_BOLD):
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
        self._p_opt = PING_OPT
        self._n_headers = N_HEADERS

        if self.config is not None:
            conf = configparser.ConfigParser()

            if not os.path.exists(self.config):
                err = 'Configuration file "{}"　was not found.'.format(
                    self.config)
                raise FileNotFoundError(err)

            conf.read(self.config)
            d = dict(conf.items(conf.sections()[conf.sections().index(HOSTS)]))

            self.names = list(d.keys())
            self.args = list(d.values())

        hostname = socket.gethostname()
        local_addr = socket.gethostbyname(hostname)

        if only_ipv6:
            if shutil.which(PING6_CMD):
                self._p_cmd = PING6_CMD
            else:
                self._p_cmd = PING_CMD
                self._p_opt += SPACE + OPT_IPV6
            ipv4 = None
        else:
            self._p_cmd = PING_CMD
            if not closed:
                try:
                    ipv4 = get_ip_info(OPT_IPV4)
                except (subprocess.TimeoutExpired,
                        subprocess.CalledProcessError):
                    ipv4 = None
            else:
                ipv4 = None

        if only_ipv4:
            if shutil.which(PING4_CMD):
                self._p_cmd = PING4_CMD
            elif not shutil.which(PING6_CMD):
                self._p_opt += SPACE + OPT_IPV4
            ipv6 = None
        else:
            if not closed:
                try:
                    ipv6 = get_ip_info(OPT_IPV6)
                except (subprocess.TimeoutExpired,
                        subprocess.CalledProcessError):
                    ipv6 = None
            else:
                ipv6 = None

        self.info = SPACE.join([FROM, hostname, '({})'.format(local_addr),
                                '\n', GLOBAL,
                                '({}, {})'.format(ipv4, ipv6)])

        self.lines = [Line(i + self._n_headers + 2, a, n, self.space)
                      for i, (a, n) in enumerate(zip(self.args, self.names))]

        self._arg_width = len(ARG)
        self._host_width = len(HOST)
        self._addr_width = len(ADDRESS)
        self._rtt_width = len(RTT)
        self._name_width = max([len(name) for name in self.names])

    def scale_char(self, rtt):
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

    def _ljust(self, target, width):
        return target.ljust(width + self.space)

    def _display_title(self):
        version = '{} v{}'.format(__title__, __version__)

        self.stdscr.addstr(0, 1, version, self.mode)
        self.stdscr.addstr(1, self.space, self.info, self.mode)

        arg = self._ljust(ARG, self._arg_width)
        name = self._ljust(NAME, self._name_width)
        host = self._ljust(HOST, self._host_width)
        addr = self._ljust(ADDRESS, self._addr_width)
        rtt = self._ljust(RTT, self._rtt_width)
        res = RESULT.ljust(self.res_width)

        if self._name_width and self.no_host:
            diff = ''.join([name])
        elif self._name_width and (not self.no_host):
            diff = ''.join([name, host])
        elif (not self._name_width) and self.no_host:
            diff = ''.join([])
        else:
            diff = ''.join([host])

        string = ''.join([arg, diff, addr, rtt, res])

        self.stdscr.addstr(self._n_headers + 1, self.space, string, self.mode)

    def _display_result(self, line):

        string = line.get_line(ARROW, self.no_host, self._arg_width,
                               self._name_width, self._host_width,
                               self._addr_width, self._rtt_width)
        self.stdscr.addstr(line.x_pos(), self.space - len(ARROW), string,
                           self.mode)

        time.sleep(self.step)

        self.stdscr.refresh()
        self.stdscr.addstr(line.x_pos(), self.space - len(SPACE),
                           string.replace(ARROW, SPACE), self.mode)

    def _display(self):
        for arg, line in zip(self.args, self.lines):
            try:
                out = subprocess.run([self._p_cmd, arg]+self._p_opt.split(),
                                     check=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL,
                                     timeout=self.timeout,
                                     ).stdout.decode()
            except (subprocess.TimeoutExpired,
                    subprocess.CalledProcessError):
                c = FAILED
            else:
                p = PingResult(out)
                c = self.scale_char(p.time)
                line.add_info(p)

            line.add_char(c)

            self._arg_width = max(len(line.arg), self._arg_width)
            self._host_width = max(len(line.host), self._host_width)
            self._addr_width = max(len(line.address), self._addr_width)
            self._rtt_width = max(len(line.rtt), self._rtt_width)

            self._display_title()
            self._display_result(line)

        for line in self.lines:
            line.reduce(self.res_width)

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        begin = time.monotonic()

        while time.monotonic() - begin < self.duration:
            self._display()
            time.sleep(self.interval)
