# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='klein_config',
      version='0.1',
      description='Configuration detection from the command line',
      url='http://gitlab.mdcatapult.io/informatics/klein/klein-config',
      author='Matt Cockayne',
      author_email='matthew.cockayne@md.catapult.org.uk',
      license='MIT',
      packages=['klein_config'],
      install_requires=[
          'argparse'
      ],
      zip_safe=True)