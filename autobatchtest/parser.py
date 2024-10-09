import sys
from os import path
import argparse


class parse(command, defaults, deltas):
    parser = argparse.ArgumentParser(description='Automated batch deplyment, tracking and result management of tests.')
    parser.add_argument('testdir', help='existing test directory')
    parser.add_argument('-s', action='store_true' ,help='run for single delta')
    parser.add_argument('-d', nargs=2, default=[], action='append', help='run with additional delta: par val')

    args = parser.parse_args(command)
    
    if not path.exists(args.testdir):
        raise Exception(f'Test directory {args.testdir:!r} not found')
    sys.path.append(p.testdir)
    if path.exists(f'{args.testdir}/{defaults}'):
        from defaults import defaults
    if path.exists(f'{args.testdir}/{deltas}'):
        from deltas import deltas

    for key, val in args.d:
        if key not in defaults:
            raise Exception(f'Invalid key found in delta {delta}')
        if type(val) != type(defaults[key]):
            raise Exception(f'Type mismatch in key {key:!r} of delta {delta}')

        type(defaults[key])(val)

    deltas = {par:type(defaults[par]) for par, val in p.d} if p.s 
         else [{**delta, **process(p.d)} for delta in deltas]

    return args