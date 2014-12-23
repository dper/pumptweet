#!/usr/bin/env python
# setup.py

from setuptools import setup

setup(name='pumptweet',
	version='1.5.0',
	description='Cross posts from Pump.io to Twitter.',
	setup_requires=['setuptools-markdown'],
	long_description_markdown_filename='README.md',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Topic :: Communications',
	],
	url='http://github.com/dper/pumptweet',
	author='Douglas Paul Perkins',
	author_email='contact@dperkins.org',
	license='MIT',
	packages=['pumptweet'],
	install_requires=[
		'pypump >= 0.5',
		'python-twitter >= 2.0',
		'BeautifulSoup >= 3.2.1',
	],
	include_package_data=True,
	scripts=[
		'pt.py',
		'pt.sh',
	],
	zip_safe=False)
