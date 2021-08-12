try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='beancount-exchangerates',
    version='3.1.0',
    description='Beancount Exchange Rates',
    packages=['beancount_exchangerates'],
    license='GPLv3',
)
