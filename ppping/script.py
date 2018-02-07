import argparse
import sys
import curses
from ppping import PPPing, __VERSION__


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*', help='hosts or addresses')
    parser.add_argument('-t', '--timeout', nargs='?', default=1, type=int, help='timeout')
    parser.add_argument('--scale', nargs='?', default=10, type=float, help='scale of RTT')
    parser.add_argument('--space', nargs='?', default=1, type=int, help='space length')
    parser.add_argument('-l', '--length', nargs='?', default=5, type=int, help='result length')
    parser.add_argument('-d', '--duration', nargs='?', default=sys.maxsize, type=float, help='duration time')
    parser.add_argument('-i', '--interval', nargs='?', default=0.8, type=float, help='interval')
    parser.add_argument('--step', nargs='?', default=0.05, type=float, help='step time per host')
    parser.add_argument('-c', '--config', type=str, help='configuration file')
    parser.add_argument('-n', '--no-host', action='store_true', help='do not display hosts')
    parser.add_argument('-v', '--version', action='store_true', help='show version and exit')

    return parser.parse_args()


def main():
    args = set_args()

    if len(sys.argv) == 1:
        sys.stderr.write('ppping: try \'ppping --help\'\n')
        return

    if args.version:
        print('ppping v{}'.format(__VERSION__))
        return

    p = PPPing(args.args, timeout=args.timeout, rtt_scale=args.scale, res_width=args.length, space=args.space,
               duration=args.duration, interval=args.interval, step=args.step, config=args.config, no_host=args.no_host)

    try:
        curses.wrapper(p.run)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
