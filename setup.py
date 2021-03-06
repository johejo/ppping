import os
from codecs import open

from setuptools import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'ppping', '__version__.py'),
          'r', 'utf-8') as f:
    exec(f.read(), about)

tests_requirements = [
    'pytest-cov', 'pytest', 'flake8'
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=readme,
    packages=['ppping'],
    python_requires='>=3.5',
    license=about['__license__'],
    url=about['__url__'],
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
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Networking :: Monitoring',
    ],
    tests_require=tests_requirements,
    platforms=['Linux', 'UNIX', 'macOS'],
)
