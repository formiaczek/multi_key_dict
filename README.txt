multi_key_dict
======================


Implementation of a multi-key dictionary, i.e.:

(key1[,key2, ..]) => value

This dictionary has a similar interface to the standard dictionary => but is extended to support multiple keys referring to the same element.

If element is created using multiple keys, e.g.:

.. code:: python

    from multi_key_dict import multi_key_dict

    k = multi_key_dict()
    k[1000, 'kilo', 'k'] = 'kilo (x1000)'

    print k[1000] # will print 'kilo (x1000)'
    print k['k'] # will also print 'kilo (x1000)'
    
    # the same way objects can be updated, deleted: 
    # and if an object is updated using one key, the new value will
    # be accessible using any other key, e.g. for example above:
    k['kilo'] = 'kilo'
    print k[1000] # will now print 'kilo' as value was updated
    
These elements can be accessed using either of those keys (e.g for read/update/deletion).

Multi-key dict provides also extended interface for iterating over items and keys (e.g. by the key type), which might be useful when creating, e.g. dictionaries with index-name key pair allowing to iterate over items using either: names or indexes.
It can be useful for many many other similar use-cases, and there is no limit to the number of keys used to map to the value.

There are few other useful methods, e.g. to iterate over dictionary (by/using) selected key type, finding other keys mapping to the same value etc. Refer to example/test code to see it in action.
