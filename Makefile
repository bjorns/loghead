all: setup test

setup:
	pip3 install -e .

cov:
	pytest --cov kuvio --cov-report=html test/

test:
	pytest --cov kuvio test/

.PHONY: all setup test
