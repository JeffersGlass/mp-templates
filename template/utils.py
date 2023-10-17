## From https://github.com/python/cpython/blob/0f9d0fb437fd206e281b84309f171f5dfe3ef0c2/Lib/re/__init__.py#L302

# SPECIAL_CHARS
# closing ')', '}' and ']'
# '-' (a range in character set)
# '&', '~', (extended character set operations)
# '#' (comment) and WHITESPACE (ignored) in verbose mode
_special_chars_map = {i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}

def escape(pattern):
    """
    Escape special characters in a string.
    """
    if isinstance(pattern, str):
        return translate(pattern, _special_chars_map) #MOD: Use alternate implementation of translate
    else:
        pattern = str(pattern, 'latin1')
        return translate(pattern, _special_chars_map).encode('latin1') #MOD: Use alternate implementation of translate
    
   
# Adaptation of str.translate, VERY ROUGHLY
def translate(s, table):
    if s is None: raise ValueError("String provided to translate must not be none")
    if len(s) == 0: return s

    ret = []
    
    for char in s:
        translation = _charmaptranslate_output(char, table)
        if translation is not None: # If value is none, char will be deleted
            ret.extend(translation)

    return ''.join(ret)

def _charmaptranslate_output(char, table):
    # Map Characters from Table
    try:
        val = table[ord(char)]
        return val
    except LookupError:
        return char
    
