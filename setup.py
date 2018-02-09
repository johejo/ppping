from setuptools import setup, find_packages

from ppping import (
    __url__, __title__, __license__, __description__, __author_email__,
    __author__, __version__,
)

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

tests_requirements = [
    'pytest-cov', 'pytest'
]

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=readme,
    packages=find_packages(),
    license=__license__,
    url=__url__,
    py_modules=['ppping'],
    entry_points={
        'console_scripts': 'ppping = ppping.script:main'
    },
    keyword=['ping-python', 'ping'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking :: Monitoring',
    ],
    tests_requires=tests_requirements,
)
