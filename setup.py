try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='beancount-exchangerates',
    version='2.0.0',
    description='Beancount Exchange Rates',
    packages=['beancount_exchangerates'],
    license='GPLv3',
)
