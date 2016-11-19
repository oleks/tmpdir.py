# Do Something With A Temporary Directory

A subprocess is often an ideal wrapper for a given task.

An often sought for wrapper is that of creating a temporary directory to make
room for some scratch-space to work with, and to purge the directory when the
task is done. Although popular programming languages have mechanisms for doing
this inside the language (e.g., a
[try-catch-finally](https://en.wikipedia.org/w/index.php?title=Exception_handling_syntax&oldid=736583603),
or the
[defer](https://web.archive.org/web/20160419202839/http://blog.golang.org/defer-panic-and-recover)
statement), there is ill support for this across language barriers. Besides,
most programming languages have a hard time offering a security barrier like
the one that a comes by merely spawning off a subprocess.

[tmpdir](tmpdir) leverages the widely accessible process abstraction instead.

[tmpdir](tmpdir) aims to be cross-platform and easy to use. This is done by
using Python, keeping the program small, and contained in one file. To use
[tmpdir](tmpdir) you can just copy it into your source tree.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/oleks/tmpdir/blob/master/tmpdir)
