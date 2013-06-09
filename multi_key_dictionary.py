'''
Created on 26 May 2013

@author: lukasz.forynski

@brief: Implementation of the multi-key dictionary.

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

class multi_key_dictionary(object):
    """ Purpose of this type is to provie a multi-key dictionary.
    Such a dictionary has a similar interface to the standard dictionary, but allows
    accessing / iterating items using multiple keys, i.e. it provices mapping from
    different types of keys (and also different keys of the same type) to the same value. 
    For example:
    
        k = multi_key_dictionary()
        k[100] = 'hundred'  # add item to the dictionary (as for normal dictionary)
        
        # but also:
        # below creates entry with two possible key types: int and str, 
        # mapping all keys to the assigned value
        k[1000, 'kilo', 'k'] = 'kilo (x1000)'
        print k[100]   # will print 'kilo (x1000)'
        print k['k']  # will also print 'kilo (x1000)'
        
        # the same way objects can be updated, and if an object is updated using one key, the new value will
        # be accessible using any other key, e.g. for example above:
        k['kilo'] = 'kilo'
        print k[1000] # will print 'kilo' as value was updated
    """
    def __getitem__(self, key):
        """ Return the value at index specified as key."""
        key_type = str(type(key))
        if (self.__dict__.has_key(key_type) and
            self.__dict__[key_type].has_key(key)
#             and self.items_dict and
#             self.items_dict.has_key(self.__dict__[key_type][key])
            ):
            return self.items_dict[self.__dict__[key_type][key]]
        else:
            raise KeyError(key)

    def __setitem__(self, keys, value):
        """ Set the value at index (or list of indexes) specified as keys."""
        if(type(keys) == type(tuple())):
            first_key = keys[0]  # if it's a list, just use the first item
        else:
            first_key = keys
        key_type = str(type(first_key)) # find the intermediate dictionary..
        if self.__dict__.has_key(key_type) and self.__dict__[key_type].has_key(first_key):
            self.items_dict[self.__dict__[key_type][first_key]] = value # .. and update the object if it exists..
        else:
            if(type(keys) != type(tuple())):
                key = keys
                keys = [keys]
            self.__add_item(value, keys) # .. or create it - if it doesn't

    def __delitem__(self, key):
        """ Called to implement deletion of self[key]."""
        key_type = str(type(key))
        if (self.__dict__.has_key(key_type) and
            self.__dict__[key_type].has_key(key) and
            self.items_dict and
            self.items_dict.has_key(self.__dict__[key_type][key])):
            intermediate_key = self.__dict__[key_type][key]

            # remove the item in main dictionary 
            del self.items_dict[intermediate_key]

            # remove all references (also pointed by other types of keys)
            # for the item that this key pointed to.
            for name, reference_dict in self.__dict__.iteritems():
                if(type(name) == type(str()) and name.find('<type') == 0):
                    ref_key = None
                    for temp_key, value in reference_dict.iteritems():
                        if value == intermediate_key:
                            ref_key = temp_key
                            break
                    if ref_key:
                        del reference_dict[ref_key]
        else:
            raise KeyError(key)

    def iteritems(self, by_key=None):
        """ Returns an iterator over the dictionary's (key, value) pairs.
            @param by_key if specified, iterator for a dictionary of it's type will be used (if available).
                   Otherwise, iterator will use a dictionary with keys whose type name is first in lexicographical order.
        """
        intermediate_key = self.__find_intermediate_key(by_key)
        if intermediate_key and self.__dict__.has_key(intermediate_key):
            for key, direct_key in self.__dict__[intermediate_key].iteritems():
                yield key, self.items_dict[direct_key]
                
    def iterkeys(self, by_key=None):
        """ Returns an iterator over the dictionary's keys.
            @param by_key if specified, iterator for a dictionary of it's type will be used (if available).
                   Otherwise, iterator will use a dictionary with keys whose type name is first in lexicographical order.
        """
        intermediate_key = self.__find_intermediate_key(by_key)
        if intermediate_key and self.__dict__.has_key(intermediate_key):
            return self.__dict__[intermediate_key].iterkeys()

    def itervalues(self, by_key=None):
        """ Returns an iterator over the dictionary's values.
            @param by_key if specified, iterator for a dictionary of it's type will be used (if available).
                   Otherwise, iterator will use a dictionary with keys whose type name is first in lexicographical order.
        """
        intermediate_key = self.__find_intermediate_key(by_key)        
        if intermediate_key and self.__dict__.has_key(intermediate_key):
            for direct_key in self.__dict__[intermediate_key].itervalues():
                yield self.items_dict[direct_key]
        
    def items(self, by_key=None):
        """ Returns a copy of the dictionary's values.
            @param by_key if specified, values will be sorted in the order for dictionary of it's type.
                 Otherwise they will be sorted in the order as for the dictionary with the key name
                 that comes first in lexicographical order (i.e.: as for '(type(xx))'
        """
        all_items = []
        intermediate_key = self.__find_intermediate_key(by_key)
        if intermediate_key and self.__dict__.has_key(intermediate_key):
            for direct_key in self.__dict__[intermediate_key].itervalues():
                all_items.append(self.items_dict[direct_key])
        return all_items

    def keys(self, by_key=None):
        """ Returns a copy of the dictionary's keys.
            @param by_key if specified, keys will be sorted in the order for dictionary of it's type.
                 Otherwise they will be sorted in the order as for the dictionary with the key name
                 that comes first in lexicographical order (i.e.: as for '(type(xx))'
        """
        intermediate_key = self.__find_intermediate_key(by_key)
        if intermediate_key and self.__dict__.has_key(intermediate_key):
            return self.__dict__[intermediate_key].keys()

    def __len__(self):
        """ Returns number of objects in dictionary."""
        length = 0
        if self.__dict__.has_key('items_dict'):
            length = len(self.items_dict)
        return length

    def __find_intermediate_key(self, by_key=None):
        """ Internal method to find the intermediate key for a requested type"""
        intermediate_key = None        
        if(by_key is not None):
            intermediate_key = str(type(by_key))
        else:
            for attr in self.__dict__.iteritems():
                if(type(attr[0]) == type(str()) and attr[0].find('<type') == 0):
                    intermediate_key = attr[0] # just use the first one available
                    break
        return intermediate_key

    def __add_item(self, item, keys=None):        
        """ Internal method to add an item to the multi-key dictionary"""
        if(not keys or not len(keys)):
            raise Exception('Error in %s.__add_item(%s, keys=tuple/list of items): need to specify a tuple/list containing at least one key!'
                            % (self.__class__.__name__, str(item)))
        direct_key = '_'.join([str(key) for key in keys]) # joined values of keys will be used as a direct key        
        for key in keys:
            key_type = str(type(key))

            # store direct key as a value in an intermediate dictionary
            if(not self.__dict__.has_key(key_type)):
                self.__setattr__(key_type, dict())
            self.__dict__[key_type][key] = direct_key
         
            # store the value in the actual dictionary
            if(not self.__dict__.has_key('items_dict')):
                self.items_dict = dict()            
            self.items_dict[direct_key] = item



def test_multintermediate_key_dictionary():    
    m = multi_key_dictionary()
    assert( len(m) == 0 ), 'expected len(m) == 0'
    
    m['aa', 12, 32, 'mmm'] = 123  # create a value with multiple keys..
    assert( len(m) == 1 ), 'expected len(m) == 1'

    m['something else'] = 'abcd'
    assert( len(m) == 2 ), 'expected len(m) == 2'

    m[23] = 0
    assert( len(m) == 3 ), 'expected len(m) == 3'
    
    # check if it's possible to read this value back using either of keys
    assert( m['aa'] == 123 ), 'expected m[\'aa\'] == 123'
    assert( m[12] == 123 ), 'expected m[12] == 123'
    assert( m[32] == 123 ), 'expected m[32] == 123'
    assert( m['mmm'] == 123 ), 'expected m[\'mmm\'] == 123'

    
    # now update value and again - confirm it back - using different keys..
    m['aa'] = 45
    assert( m['aa'] == 45 ), 'expected m[\'aa\'] == 45'
    assert( m[12] == 45 ), 'expected m[12] == 45'
    assert( m[32] == 45 ), 'expected m[32] == 45'
    assert( m['mmm'] == 45 ), 'expected m[\'mmm\'] == 45'
    
    m[12] = 4
    assert( m['aa'] == 4 ), 'expected m[\'aa\'] == 4'
    assert( m[12] == 4 ), 'expected m[12] == 4'

    # now test deletion..
    curr_len = len(m)
    del m[12]
    assert( len(m) == curr_len - 1 ), 'expected len(m) == %d' % (curr_len - 1)

    # try again 
    try:
        del m['aa']
        assert(False), 'cant remove again: item m[\'aa\'] should not exist!'
    except KeyError, err:
        pass

    # try to access non-existing 
    try:
        k =  m['aa']
        assert(False), 'removed item m[\'aa\'] should exist!'
    except KeyError, err:
        pass

    # try to access non-existing with a different key 
    try:
        k =  m[12]
        assert(False), 'removed item m[12] should exist!'
    except KeyError, err:
        pass

    # prepare for other tests (also testing creation of new items)
    tst_range = range(10, 40) + range(50, 70)
    for i in tst_range:
        m[i] = i # will create a dictionary, where keys are same as items

    # test iteritems()
    for key, item in m.iteritems(int()):
        assert(key == item), 'iteritems(int()): Expected %d, but received %d' % (key, item)

    # test iterkeys()
    curr_index_in_range = 0
    for key in m.iterkeys(int()):
        expected = tst_range[curr_index_in_range]
        assert (key == expected), 'iterkeys(int): Expected %d, but received %d' % (expected, key)
        curr_index_in_range += 1

    #test itervalues()
    curr_index_in_range = 0
    for value in m.itervalues(int()):
        expected = tst_range[curr_index_in_range]
        assert (value == expected), 'itervalues(int): Expected %d, but received %d' % (expected, value)
        curr_index_in_range += 1

    # test items()
    assert (m.items(int()) == tst_range), 'm.items(int()) is not as expected.'

    # test keys()
    assert (m.keys(int()) == tst_range), 'm.keys(int()) is not as expected.'

    print 'All test passed OK!'


if __name__ == '__main__':
    try:
        test_multintermediate_key_dictionary()
    except Exception, err:
        print 'Error: ', err
    except KeyboardInterrupt:
        print '\n(interrupted by user)'

