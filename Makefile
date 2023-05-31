all: setup check test

setup:
	pip3 install -e .

cov:
	pytest --cov loghead --cov-report=html test/

check:
	pylint --fail-under 9.9 loghead

test:
	pytest --cov loghead test/


.PHONY: all setup test
