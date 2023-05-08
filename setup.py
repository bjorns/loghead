from setuptools import setup, find_packages

setup(
	name='hirsi',
	version='0.0.1',
	url='https://github.com/bjorns/hirsi.git',
	author='Bjorn Skoglund',
	author_email='hirsiadmin@fastmail.com',
	description='A kind logger',
	packages=['hirsi'],
	install_requires=[
		'PyYaml >= 6.0'
	],
)
