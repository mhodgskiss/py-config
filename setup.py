# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='klein_config',
      version='1.0.2',
      description='Configuration detection from the command line',
      url='http://gitlab.mdcatapult.io/informatics/klein/klein-config',
      author='Matt Cockayne',
      author_email='matthew.cockayne@md.catapult.org.uk',
      license='MIT',
      packages=['klein_config'],
      install_requires=[
          'argparse',
          'pyyaml',
          'klein_util'
      ],
      zip_safe=True)