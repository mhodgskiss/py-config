# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='klein_config',
      version='2.0.1',
      description='Configuration detection from the command line',
      url='http://gitlab.mdcatapult.io/informatics/klein/klein-config',
      author='Matt Cockayne',
      author_email='matthew.cockayne@md.catapult.org.uk',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'':'src'},
      install_requires=[
          'argparse',
          'pyyaml',
          'pyhocon',
          'klein_util'
      ],
      zip_safe=True)