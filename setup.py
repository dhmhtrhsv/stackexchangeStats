from setuptools import setup

setup(name='stackexchangeStats',
      version='1.0',
      description='Stackexchange Statistics',
      author='Dimitris Varoutas',
      author_email='dhmhtrhsv@hotmail.com',
      packages=['stackexchangeStats'],
      install_requires=[
            'requests',
            'json2html',
      ],
      )