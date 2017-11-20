PROJECT := python-tbstracker
GIT_HUB := https://github.com/fujexo/python-tbstracker

include pyproject/Makefile

test_ext:
	echo Execute custom tests
