try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='beancount-exchangerates',
    version='5.1.1',
    description='Beancount Exchange Rates',
    packages=['beancount_exchangerates'],
    license='GPLv3',
)
