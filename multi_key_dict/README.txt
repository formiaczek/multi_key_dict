multi_key_dict
======================


Implementation of a multi-key dictionary.

This kind of dictionary has a similar interface to the standard dictionary,

and indeed if used with single key key elements - it's behaviour is the same as for a standard dict.

However it also allows for creation of elements using multiple keys (using tuples/lists). Such elements can be accessed using either of those keys (e.g for read/update/deletion). 
Multi-key dict provides also extended interface for iterating over items and keys (e.g. by the key type), which might be useful when creating, e.g. dictionaries with index-name key pair allowing to iterate over items using either: names or indexes.
It can be useful for many many other similar use-cases, and there is no limit to the number of keys used to map to the value.

There are also methods to get other keys that map to the same element and others. Refer to examples and test code to see it in action.
