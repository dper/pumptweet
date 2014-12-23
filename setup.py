#!/usr/bin/env python
# setup.py

from setuptools import setup

setup(name='pumptweet',
	version='1.4.3',
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
		'pypump>=0.5',
		'python-twitter',
		'BeautifulSoup',
	],
	include_package_data=True,
	scripts=[
		'pumptweet/pt.py',
		'pumptweet/pt.sh',
	],
	zip_safe=False)
