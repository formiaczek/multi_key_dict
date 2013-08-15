'''
Created on 5 Jun 2013

@author: lukasz.forynski

@brief Simple text progress-bar.

https://github.com/formiaczek/python_data_structures
___________________________________

 Copyright (c) 2013 Lukasz Forynski <lukasz.forynski@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sub-license, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''


import sys
import time


class text_progress_bar(object):
    ## Init method.
    # @param length_in_chars lenght of the progress bar.
    def __init__(self, length_in_chars, str_to_write_on_finished = '\n'):
        self.length = length_in_chars
        self.str_on_finished = str_to_write_on_finished
        self.reset()

    ## resets the progress bar
    def reset(self):
        self.current = 0
        self.total = 0
        self.description = ''
        self.bar = list('.' * self.length)
    
    ## method to set the progress description
    # @description test to be displayed next to the progress bar
    # (e.g. name of the task for which the progress is displayed)
    def set_description(self, description):
        if len(description):
            self.description = ': %s' % description

    ## Callback to indicate (update and display) the progress
    # @param current - current value of the progress
    # @param total total value (i.e. he number current is converging to)
    def progress_callback(self, current, total):
        if self.total != total:
            self.total = total
        
        if total:
            new_current = (current * self.length)
            new_current /= self.total
            if new_current > self.current:
                for i in xrange(self.current,new_current):
                    self.bar[i] = '='
                self.current = new_current
            sys.stdout.write('\r[%s] %s (%d/%d)  ' % (''.join(self.bar), 
                                                 self.description,
                                                 current, 
                                                 total))
            if current == self.total:
                self.reset()
                sys.stdout.write('\n')

def test_progress_bar():
    b = text_progress_bar(30)
    b.set_description('testing progress')
    for i in xrange(0, 335+1): # say our task is from 0-335 steps..
        b.progress_callback(i, 335)
        time.sleep(0.025)


if __name__ == '__main__':
    test_progress_bar()
