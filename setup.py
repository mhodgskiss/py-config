# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='klein_postgres',
      version='0.0.1',
      description='PostgreSQL integration',
      url='http://gitlab.mdcatapult.io/informatics/klein/klein_postgres',
      author='Matt Cockayne',
      author_email='matthew.cockayne@md.catapult.org.uk',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'':'src'},
      install_requires=[
          'klein_config',
          'psycopg2-binary'
      ],
      zip_safe=True)