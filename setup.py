#!python

from distutils.core import setup

long_descr=''

with open('README.txt') as readme:
    long_descr = readme.read()

setup(name='multi_key_dict',
      version='2.0.3',
      description='Multi key dictionary implementation',
      author='Lukasz Forynski',
      author_email='lukasz.forynski@gmail.com',
      url='https://github.com/formiaczek/multi_key_dict',
      py_modules=['multi_key_dict'],
      license='License :: OSI Approved :: MIT License (http://opensource.org/licenses/MIT)',
      long_description=long_descr,
      classifiers=[
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Development Status :: 5 - Production/Stable',
                   'Operating System :: OS Independent',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries :: Python Modules'
                   ]
      )
