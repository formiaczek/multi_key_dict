#!python

from distutils.core import setup

long_descr=''

with open('README.txt') as readme:
    long_descr = readme.read()

setup(name='text_progress_bar',
      version='1.0.1',
      description='Simple text progress bar',
      author='Lukasz Forynski',
      author_email='lukasz.forynski@gmail.com',
      url='https://github.com/formiaczek/python_data_structures',
      py_modules=['text_progress_bar'],
      license=['License :: OSI Approved :: MIT License (http://opensource.org/licenses/MIT)'],
      long_description=long_descr,
      classifiers=[
                   'Programming Language :: Python',
                   'License :: OSI Approved :: MIT License',
                   'Development Status :: 4 - Beta',
                   'Operating System :: OS Independent',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries :: Python Modules'
                   ]
      )
