An adaptation of CPython's `Template` class suitable for Micropython.

## Usage

To try this out in PyScript+Micropthon:
  1. Clone this repository
  2. Open `examples/helloworld.html` in your live server of choice

To include this in your own experiments, copy the `template` folder into your project.

## Notes

Adding `Template` involves bringing over, and slightly modifying, a number of additional CPython clases and functions, including:
  * `ChainMap`
  * `MutableMapping`
  * `Mapping`
  * `re.escape` (as `utils.escape`)

As well as re-implementing or otherwise working around:
  * `string.translate` (as `utils.translate`)
  * `re.finditer` (as `utils.finditer`)

A number of concessions have been made:

  * In CPython, it is possible to [subclass `Template`](https://docs.python.org/3/library/string.html#string.Template) to customize various behaviors. This is not currently implemented.
  * `Mapping` no longer inherits from `abc.Collection`, which only provides Abstract methods. This breaks some inheritance checks.
  * In CPython `string.translate` is implemented in C, in a way that carefully accomodates unicode characters. It has been re-implemented here in Python, using a simple `ord()` lookup, with the performance penalties that implies.