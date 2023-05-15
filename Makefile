all: setup test

setup:
	pip3 install -e .

test:
	pytest --cov kuvio test/

.PHONY: all setup test
