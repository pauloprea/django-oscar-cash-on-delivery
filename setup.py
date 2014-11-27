#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='django-oscar-cash-on-delivery',
      version='0.1',
      url='https://github.com/pauloprea/django-oscar-cash-on-delivery',
      author="Paul Oprea",
      author_email="atreidesone@gmail.com",
      description="Cash on delivery payment module for django-oscar",
      long_description=open('README.rst').read(),
      keywords="Payment, COD, Cash,",
      license='BSD',
      packages=find_packages(exclude=['sandbox*', 'tests*']),
      include_package_data=True,
      install_requires=['django-oscar>=0.6.4,<1.1'],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )