SHELL:=/usr/bin/env bash

test: \
	test_no_args \
	test_keepwd_no_other_args

cwd=$(shell pwd)

test_no_args:
	file `./tmpdir pwd` | grep "No such file or directory" > /dev/null

test_keepwd_no_other_args:
	./tmpdir --keepwd pwd | diff -u - <(echo $(cwd)) > /dev/null
