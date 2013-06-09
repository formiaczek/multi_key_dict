'''
Created on 9 Jun 2013

@author: lukasz.forynski

@brief: Function to get some trace information about the exception-rising code,
        when called from exception handler. 
       
       This information includes:
        - module name
        - class name (if exception executed in the method)
        - line number
        
    This might be more useful (and logical) than what's provided with traceback
    which gives filenames, line numbers and code snippets

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


import inspect
import sys
import os


def raising_code_info():
    code_info = ''
    try:    
        frames = inspect.trace()
        if(len(frames)):
            full_method_name = frames[0][4][0].rstrip('\n\r').strip()
            line_number      = frames[1][2]
            module_name      = frames[0][0].f_globals['__name__']
            if(module_name == '__main__'):
                module_name = os.path.basename(sys.argv[0]).replace('.py','')
            class_name = ''
            obj_name_dot_method = full_method_name.split('.', 1)
            if len(obj_name_dot_method) > 1:
                obj_name, full_method_name = obj_name_dot_method
                try:
                    class_name = frames[0][0].f_locals[obj_name].__class__.__name__
                except:
                    pass
            method_name = module_name + '.'
            if len(class_name) > 0:
                method_name += class_name + '.'
            method_name += full_method_name
            code_info = '%s, line %d' % (method_name, line_number)
    finally:
        del frames
        sys.exc_clear()
    return code_info


def function1():
    print 1/0

class AClass(object):    
    def method2(self):
        a = []
        a[3] = 1

def try_it_out():
    # try it with a function
    try:
        function1()
    except Exception, what:
        print '%s: \"%s\"' % (raising_code_info(), what)

    # try it with a method
    try:
        my_obj_name = AClass()
        my_obj_name.method2()       
    except Exception, what:
        print '%s: \"%s\"' % (raising_code_info(), what)

if __name__ == '__main__':
     try_it_out()
