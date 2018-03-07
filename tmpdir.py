#!/usr/bin/env python3

# Do Something With A Temporary Directory
# See also https://github.com/oleks/tmpdir.py

# Copyright (c) 2016 Oleks <oleks@oleks.info>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import os.path
import shutil
import subprocess
import sys
import tempfile

from contextlib import contextmanager
from typing import List


@contextmanager
def tmpdir(copy=None,
           dir=tempfile.gettempdir(),
           prefix=tempfile.gettempprefix(),
           suffix=""):

    tmp = tempfile.mkdtemp(dir=dir, prefix=prefix, suffix=suffix)

    try:
        if copy:
            if os.path.isfile(copy):
                shutil.copy2(copy, tmp)
            else:
                copytree(copy, tmp)

        yield tmp

    finally:
        shutil.rmtree(tmp)


# http://stackoverflow.com/a/12514470/5801152
def copytree(src: str, dst: str, symlinks: bool) -> None:
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks)
        else:
            shutil.copy2(s, d)


def main_with_args(args):
    dict_args = vars(args)
    tmpdir_args = { k: dict_args[k] for k in ['copy', 'dir', 'prefix', 'suffix'] }

    with tmpdir(**tmpdir_args) as tmp:
        cwd = "."

        had_tmpdir = False
        for i, arg in enumerate(args.args):
            if arg == "%%TMPDIR":
                args.args[i] = tmp
                had_tmpdir = True

        if (args.cwd or not had_tmpdir) and not args.keepwd:
            cwd = tmp

        env = os.environ.copy()
        if args.env:
            env["TMPDIR"] = tmp

        command = [args.command] + args.args

        proc = subprocess.Popen(command, cwd=cwd, env=env)
        return proc.wait()


def parse_main_args(args: List[str]=sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
Do something with a temporary directory (TMPDIR).
""")
    parser.add_argument(
        "command", metavar="COMMAND",
        help="""
the command to execute in the current environment, with the
current working directory; if %%TMPDIR does not appear once
among its arguments, change working directory to TMPDIR
""")
    parser.add_argument(
        "args", metavar="...", nargs=argparse.REMAINDER,
        help="""
arguments to pass to the command; all %%%%TMPDIR arguments
will be replaced by the absolute path to the created TMPDIR
""")
    parser.add_argument(
        "-d", "--dir", metavar="PATH",
        help="""
create the temporary directory under PATH
""")
    parser.add_argument(
        "-p", "--prefix", metavar="TEXT",
        help="""
create the temporary directory with directory name prefix TEXT
""")
    parser.add_argument(
        "-s", "--suffix", metavar="TEXT",
        help="""
create the temporary directory with directory name suffix TEXT
""")
    parser.add_argument(
        "-c", "--copy", metavar="PATH",
        help="""
copy PATH (recursively) into TMPDIR before running COMMAND
""")
    parser.add_argument(
        "-g", "--cwd", action="store_true",
        help="""
cd in to TMPDIR before executing COMMAND
""")
    parser.add_argument(
        "-k", "--keepwd", action="store_true",
        help="""
stay in current working directory
""")
    parser.add_argument(
        "-e", "--env", action="store_true",
        help="""
set the environment variable TMPDIR to the absolute path to
the created tmpdir
""")
    return parser.parse_args(args)


def main():
    args = parse_main_args()
    sys.exit(main_with_args(args))


if __name__ == "__main__":
    main()
