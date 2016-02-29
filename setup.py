import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

prjdir = os.path.dirname(__file__)
def read(filename):
    return open(os.path.join(prjdir, filename)).read()

LONG_DESC = read('README.md') + '\nCHANGES\n=======\n\n' + read('CHANGES')

install_requires = [
    'gevent==1.1rc5',
    'greenlet==0.4.9',
    'kazoo==2.2.1',
    'pykafka==2.2.1',
    'six==1.10.0',
    'tabulate==0.7.5',
    'termcolor==1.1.0',
    'wheel==0.24.0',
]

base_dir = os.path.dirname(os.path.realpath(__file__))

setup(
    name='kafkalavista',
    version='0.1.0',
    author='Nagarjuna Kumar',
    author_email='nagarjuna.412@gmail.com',
    description='Simple CLI to view and monitor kafka topics and offsets',
    long_description=LONG_DESC,
    licence='MIT',
    url='http://www.github.com/nk412/kafkalavista',
    packages=['kafkalavista'],
    install_requires=install_requires,
    setup_requires=['nose>=1.0']
)
