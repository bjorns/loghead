all: setup test

setup:
	pip3 install -e .

cov:
	pytest --cov loghead --cov-report=html test/

check:
	pylint loghead

test:
	pytest --cov loghead test/


.PHONY: all setup test
