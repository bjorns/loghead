from setuptools import setup, find_packages

setup(
	name='kuviolog',
	version='0.0.1',
	url='https://github.com/bjorns/kuviolog.git',
	author='Bjorn Skoglund',
	author_email='kuvioadmin@fastmail.com',
	description='A kind logger',
	packages=['kuvio'],
	install_requires=[
		'PyYaml >= 6.0'
	],
)
