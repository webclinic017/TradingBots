#!/usr/bin/env python
from setuptools import setup
from os.path import dirname, join, isfile
from shutil import copyfile

here = dirname(__file__)

setup(name='herald-cap-money-printing-toolbelt',
      version='0.1',
      description='Simple scripts for viewing your growing crypto wealth.',
      long_description=open(join(here, 'README.md')).read(),
      author='Kirk',
      author_email='kirkportas@gmail.com',
      url='',
      install_requires=[
          'requests',
          'ccxt',
          'coinbase'
      ]
      )

if not isfile('settings.py'):
    copyfile('_settings_base.py', 'settings.py')
print("\n**** \nImportant!!!\nEdit settings.py before starting the script.\n****")