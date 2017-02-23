SHELL:=/usr/bin/env bash

test: \
	test_no_args \
	test_retval \
	test_keepwd_no_other_args \
	test_dir_dot \
	test_dir_tmpdir

cwd=$(shell pwd)

test_no_args:
	file `./tmpdir.py pwd` | \
		grep "No such file or directory" > /dev/null

test_retval:
	./tmpdir.py bash -c "exit 1"; [[ $$? -eq 1 ]]

test_keepwd_no_other_args:
	./tmpdir.py --keepwd pwd | \
		diff -u - <(echo $(cwd))

test_dir_dot:
	./tmpdir.py --dir . bash -c "cd .. && pwd" | \
		diff -u - <(echo $(cwd))

test_dir_tmpdir:
	"$(cwd)/tmpdir.py" --env bash -c \
		"\"$(cwd)/tmpdir.py\" --dir \"\$$TMPDIR\" bash -c \"cd .. && pwd\" | diff -u - <(echo \$$TMPDIR)"
