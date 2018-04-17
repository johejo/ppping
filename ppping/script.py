import argparse
import sys
import curses
from ppping import PPPing, __version__, __title__


def set_args():
    p = argparse.ArgumentParser()
    p.add_argument('args', nargs='*', help='hosts or addresses')
    p.add_argument('-t', '--timeout', nargs='?', default=1,
                   type=int, help='timeout')
    p.add_argument('-s', '--scale', nargs='?', default=10,
                   type=float, help='scale of RTT')
    p.add_argument('--space', nargs='?', default=1,
                   type=int, help='space length')
    p.add_argument('-l', '--length', nargs='?', default=5,
                   type=int, help='result length')
    p.add_argument('-d', '--duration', nargs='?', default=sys.maxsize,
                   type=float, help='duration time')
    p.add_argument('-i', '--interval', nargs='?', default=0.8,
                   type=float, help='interval')
    p.add_argument('--step', nargs='?', default=0.05,
                   type=float, help='step time per host')
    p.add_argument('-c', '--config', type=str, help='configuration filename')
    p.add_argument('-n', '--no-host', action='store_true',
                   help='do not display hosts')
    p.add_argument('-C', '--closed', action='store_true',
                   help='do not acquire global IP address')
    p.add_argument('-4', '--ipv4', action='store_true', help='use only ipv4')
    p.add_argument('-6', '--ipv6', action='store_true', help='use only ipv6')
    p.add_argument('-v', '--version', action='version', version=__version__)

    return p.parse_args()


def main():
    args = set_args()

    if len(sys.argv) == 1:
        sys.stderr.write('{0}: try \'{0} --help\'\n'.format(__title__))
        exit(1)

    ppping = PPPing(args.args, timeout=args.timeout, rtt_scale=args.scale,
                    res_width=args.length, space=args.space,
                    duration=args.duration, interval=args.interval,
                    step=args.step, config=args.config, closed=args.closed,
                    no_host=args.no_host, only_ipv4=args.ipv4,
                    only_ipv6=args.ipv6)

    try:
        curses.wrapper(ppping.run)
    except (KeyboardInterrupt, ProcessLookupError):
        exit(0)
