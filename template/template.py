# From https://github.com/python/cpython/blob/main/Lib/string.py
# Modifications noted in comments with MOD:

import re as _re
from .chainmap import ChainMap as _ChainMap
from .utils import escape

_sentinel_dict = {}

class Template:
    """A string class for supporting $-substitutions."""

    delimiter = '$'
    # r'[a-z]' matches to non-ASCII letters when used with IGNORECASE, but
    # without the ASCII flag.  We can't add re.ASCII to flags because of
    # backward compatibility.  So we use the ?a local flag and [a-z] pattern.
    # See https://bugs.python.org/issue31672
    idpattern = r'[_a-zA-Z][_a-zA-Z0-9]*'
    braceidpattern = None
    #flags = _re.IGNORECASE # MOD: MP RE does not use flags; added uppercase letter to the idpattern above

           

    def __init__(self, template):
        self.template = template

        # MOD: The following logic was previously in __init_subclass__, but moved
        # here due to difference in inheritnace
        delim = escape(self.delimiter)
        id = self.idpattern
        bid = self.braceidpattern or self.idpattern
        # MOD: Raw f strings not permitted in Micropython
        self._pattern = f"{delim}(({delim})|({id})|{{({bid})}}|())"

        # Escape sequence of two delimiters #Escaped
        # delimiter and a Python identifier #Named
        # delimiter and a braced identifier #Braced
        # Other ill-formed delimiter exprs #Invalid

        self.pattern = _re.compile(self._pattern)

    # Search for $$, $identifier, ${identifier}, and any bare $'s

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(keepends=True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' %
                         (lineno, colno))

    def substitute(self, mapping=_sentinel_dict, **kws): # MOD: No position-only arguments
        if mapping is _sentinel_dict:
            mapping = kws
        elif kws:
            mapping = _ChainMap(kws, mapping)
        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group(3)
            if named is not None:
                return str(mapping[named])
            braced = mo.group(4)
            if braced is not None:
                return str(mapping[braced.strip('{}')])
            if mo.group(1) is not None:
                return self.delimiter
            if mo.group(4) is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return _re.sub(self.pattern, convert, self.template)

    def safe_substitute(self, mapping=_sentinel_dict, **kws): # MOD: No position-only arguments
        if mapping is _sentinel_dict:
            mapping = kws
        elif kws:
            mapping = _ChainMap(kws, mapping)
        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group(3)
            if named is not None:
                try:
                    return str(mapping[named])
                except KeyError:
                    return mo.group(0)
            braced = mo.group(4)
            if braced is not None:
                try:
                    return str(mapping[braced.strip('{}')])
                except KeyError:
                        return mo.group(0)
            if mo.group(1) is not None:
                return self.delimiter
            if mo.group(4) is not None:
                return self.group(0)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return _re.sub(self.pattern, convert, self.template)

    def is_valid(self):
        for mo in self.pattern.finditer(self.template):
            if mo.group('invalid') is not None:
                return False
            if (mo.group('named') is None
                and mo.group('braced') is None
                and mo.group('escaped') is None):
                # If all the groups are None, there must be
                # another group we're not expecting
                raise ValueError('Unrecognized named group in pattern',
                    self.pattern)
        return True

    def get_identifiers(self):
        ids = []
        for mo in self.pattern.finditer(self.template):
            named = mo.group('named') or mo.group('braced')
            if named is not None and named not in ids:
                # add a named group only the first time it appears
                ids.append(named)
            elif (named is None
                and mo.group('invalid') is None
                and mo.group('escaped') is None):
                # If all the groups are None, there must be
                # another group we're not expecting
                raise ValueError('Unrecognized named group in pattern',
                    self.pattern)
        return ids

# Initialize Template.pattern.  __init_subclass__() is automatically called
# only for subclasses, not for the Template class itself.
# MOD: See notes in __init__ above Template.__init_subclass__()