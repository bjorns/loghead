from setuptools import setup, find_packages

setup(
	name='loghead',
	version='0.0.1',
	url='https://github.com/bjorns/loghead.git',
	author='Bjorn Skoglund',
	author_email='logheadadmin@fastmail.com',
	description='A kind logger',
	packages=['loghead'],
	install_requires=[
		'PyYaml >= 6.0',
		'watchdog>=3.0.0'
	],
	tests_require=[
		'pylint==2.17.4',
		'pytest==7.3.1',
		'pytest-cov==4.0.0'
	]
)
