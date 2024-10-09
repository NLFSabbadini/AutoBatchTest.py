import time
import json
import sys
import os
import subprocess
from .parse import *
import sys
from os import path
import argparse


def parse(command, defaults, deltas):
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

    gamma = {key:val for key, val in args.d}
    deltas = [gamma] if args.s else [{**delta, **gamma} for delta in deltas]

    for delta in deltas:
        for key, val in delta.items():
            if key not in defaults:
                raise Exception(f'Invalid key found in delta {delta}')
            delta[key] = type(defaults[key])(val)

    argsl = [{**defaults, **delta} for delta in deltas]
    subdirl = [f'{testdir}/{hash(f'{args}{time.time_ns()}')}' for args in argsl]
    return testdir, subdir, argsl


def run(command=sys.argv, defaults={}, deltas=[{}], deploy='sh', preamble='', python=sys.executable):
    testdir, subdirl, argsl = parse(command, defaults, deltas)
    for subdir, args in zip(subdirl, argsl):
        request = f'''
        {deploy} << SH
        {preamble}
        {python} << PY
        import sys
        sys.path.append({testdir:!r})
        from job import job
        job({subdir:!r}, {args})
        PY
        SH'''

        os.makedirs(subdir, exist_ok=True)
        with open(path.join(subdir,'args.json'),'w') as file:
            json.dump(args, file, indent=4)
        subprocess.run(request, shell=True)