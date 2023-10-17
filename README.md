A functional, if a little bodgey, implementation of CPython's `Template` class suitable for Micropython.

This involves bringing over, and slightly modifying, a number of additional CPython clases and functions, including:
  * `ChainMap`
  * `MutableMapping`
  * `Mapping`
  * `string.translate`
  * `re.escape`

A number of concessions have been made:

  * In CPython, it is possible to [subclass `Template`](https://docs.python.org/3/library/string.html#string.Template) to customize various behaviors. This is not currently implemented.
  * To put a backstop on inheritance, `Mapping` no longer inherits from `abc.Collection`, which only provides Abstract methods. This breaks some inheritance checks.
  * In CPython `string.translate` is implemented in C, in a way that carefully accomodates unicode characters. It has been re-implemented here in Python, using