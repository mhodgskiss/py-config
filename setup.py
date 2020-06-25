# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


__version__ = ''
exec(open("./src/version.py").read())
if __version__ == '':
    raise RuntimeError("unable to find application version")

setup(name='klein_config',
      version=__version__,
      description='Configuration detection from the command line',
      url='http://gitlab.mdcatapult.io/informatics/klein/klein-config',
      author='Matt Cockayne',
      author_email='matthew.cockayne@md.catapult.org.uk',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          'pyyaml>=5.1',
          'pyhocon'
      ],
      zip_safe=True)
