from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name='ppping',
    version='0.1.2',
    author='Mitsuo Heijo',
    author_email='mitsuo_h@outlook.com',
    description='Petty Plain Ping',
    long_description=readme,
    packages=find_packages(),
    license='MIT',
    url='http://github.com/johejo/ppping',
    py_modules=['ppping'],
    entry_points={
        'console_scripts': 'ppping = ppping.script:main'
    },
    keyword=['ping-python', 'ping'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
