import argparse
import sys
import curses
from ppping import PPPing, __VERSION__


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*', help='Hosts or Addresses')
    parser.add_argument('-t', '--timeout', nargs='?', default=1, type=int, help='Timeout')
    parser.add_argument('--scale', nargs='?', default=10, type=int, help='RTT Scale')
    parser.add_argument('--space', nargs='?', default=1, type=int, help='Space Size')
    parser.add_argument('-l', '--length', nargs='?', default=5, type=int, help='Result Length')
    parser.add_argument('-d', '--duration', nargs='?', default=sys.maxsize, type=int, help='Duration')
    parser.add_argument('-c', '--config', type=str, help='Configuration file')
    parser.add_argument('-v', '--version', action='store_true', help='Version')

    return parser.parse_args()


def main():
    args = set_args()

    if len(sys.argv) == 1:
        sys.stderr.write('ppping: try \'ppping --help\'\n')
        return

    if args.version:
        print('ppping v{}'.format(__VERSION__))
        return

    p = PPPing(args.args, args.timeout, args.scale, args.length, args.space, args.duration, args.config)

    try:
        curses.wrapper(p.run)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
