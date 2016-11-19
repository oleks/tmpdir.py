# Do Something With A Temporary Directory

A subprocess is often an ideal wrapper for a given task.

An often sought for wrapper is that of creating a temporary directory to make
room for some scratch-space to work with, and to purge the directory when the
task is done.

Although popular programming languages have mechanisms for doing this inside
the language (e.g., a
[try-catch-finally](https://en.wikipedia.org/w/index.php?title=Exception_handling_syntax&oldid=736583603),
or
[defer](https://web.archive.org/web/20160419202839/http://blog.golang.org/defer-panic-and-recover)
statement), there is ill support for this across language barriers. Besides,
most programming languages have a hard time offering a barrier like the one
offered by a good old subprocess.

[tmpdir](tmpdir) leverages the widely accessible process abstraction instead.

[tmpdir](tmpdir) aims to be cross-platform and easy to use: [tmpdir](tmpdir) is
a small, self-contained Python executable. This makes it easy to just copy
[tmpdir](tmpdir) into your source tree and use it. (The [Makefile](Makefile) is
for testing purposes only.)

[![Build Status](https://travis-ci.org/oleks/tmpdir.svg?branch=master)](https://travis-ci.org/oleks/tmpdir)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/oleks/tmpdir/blob/master/tmpdir)

## Exploratory Examples

The following examples assume that you've added the path to [tmpdir](tmpdir) to
your `PATH` environment variable.

Prefixing your command with `tmpdir` will change working directory to the
created temporary directory and execute the command in there:

```
~$ tmpdir bash
/tmp/tmpPOFIGL$ exit
~$ tmpdir pwd
/tmp/tmp7x_3Qj
~$ file /tmp/tmpdJCHRW
/tmp/tmpdJCHRW: cannot open `/tmp/tmpdJCHRW' (No such file or directory)
~$ file /tmp/tmp7x_3Qj
/tmp/tmp7x_3Qj: cannot open `/tmp/tmp7x_3Qj' (No such file or directory)
```

You can also copy a file or directory (e.g., student submission) into the temporary
directory with the `-c|--copy` argument:

```
~$ tmpdir --copy /etc/passwd bash
/tmp/tmpLVfhmy$ ls
passwd
/tmp/tmpLVfhmy$ diff -u passwd /etc/passwd
/tmp/tmpLVfhmy$
```

Changing the working directory might be intrusive to your scripts, so there is
a `-k|--keepwd` option. To get a hold of the path to the working directory, you
either list the special argument name `%%TMPDIR`, or use the `-e|--env`
argument to store it in a `TMPDIR` environment variable.

This means that the following commands have a similar effect

```
~$ tmpdir --keepwd echo %%TMPDIR
/tmp/tmpfSuRru
~$ tmpdir --keepwd --env bash -c "echo \$TMPDIR"
/tmp/tmp6j4SWa
~$
```

The argument `%%TMPDIR` is welcome to appear more than once in the argument
list.

You can mandate the parent directory of your temporary directory using the
`-d|--dir` argument, and the prefix and postfix of the directory name using the
`-p|--prefix` and `-s|--suffix` arguments.
