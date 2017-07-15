try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

from esprima import version


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()
    except IOError:
        return ''


setup(
    name='esprima',
    version=version,
    author='German M. Bravo (Kronuz)',
    author_email='german.mb@gmail.com',
    packages=[
        'esprima',
    ],
    url='http://github.com/Kronuz/exprima-python',
    license='BSD',
    keywords='esprima ecmascript javascript parser',
    description="ECMAScript parsing infrastructure for multipurpose analysis in Python",
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'esprima = esprima.__main__:main',
        ]
    },
)
