import argparse
import sys
import curses
from ppping import PPPing


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*', help='Hosts or Addresses')
    parser.add_argument('-t', '--timeout', nargs='?', default=5, help='Timeout')
    parser.add_argument('--scale', nargs='?', default=10, help='RTT Scale')
    parser.add_argument('--space', nargs='?', default=2, help='Space Size')
    parser.add_argument('-l', '--length', nargs='?', default=5, help='Result Length')
    parser.add_argument('-d', '--duration', nargs='?', default=sys.maxsize, help='Duration')

    return parser.parse_args()


def main():
    args = set_args()
    if len(sys.argv) == 1:
        sys.stderr.write('ppping: try \'ppping --help\'\n')
    p = PPPing(args.args, args.timeout, args.scale, args.length, args.space, args.duration)
    try:
        curses.wrapper(p.run)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
