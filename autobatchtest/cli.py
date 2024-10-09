import argparse

parser = argparse.ArgumentParser(description='Automated batch deplyment, tracking and result management of tests.')
parser.add_argument('testdir', help='existing test directory')
parser.add_argument('-s', action='store_true' ,help='run for single delta')
parser.add_argument('-d', nargs=2, default=[], action='append', help='run with additional delta: par val')

print(parser.parse_args())