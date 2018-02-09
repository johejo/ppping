from argparse import ArgumentParser
import sys
import curses
from ppping import PPPing, __version__, __title__


def set_args():
    p = ArgumentParser()
    p.add_argument('args', nargs='*', help='hosts or addresses')
    p.add_argument('-t', '--timeout', nargs='?', default=1,
                   type=int, help='timeout')
    p.add_argument('--scale', nargs='?', default=10,
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
    p.add_argument('-c', '--config', type=str, help='configuration file')
    p.add_argument('-n', '--no-host', action='store_true',
                   help='do not display hosts')
    p.add_argument('-v', '--version', action='version', version=__version__,
                   help='show version and exit')

    return p.parse_args()


def main():
    args = set_args()

    if len(sys.argv) == 1:
        sys.stderr.write('{0}: try \'{0} --help\'\n'.format(__title__))
        exit()

    p = PPPing(args.args, timeout=args.timeout, rtt_scale=args.scale,
               res_width=args.length, space=args.space, duration=args.duration,
               interval=args.interval, step=args.step,
               config=args.config, no_host=args.no_host)

    try:
        curses.wrapper(p.run)
    except KeyboardInterrupt:
        exit()
