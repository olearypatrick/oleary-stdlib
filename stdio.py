"""
stdio.py

The stdio module supports reading from standard input and writing to sys.stdout.
"""
    
import sys
import re

# ----------------------------------------------------------------------------------------------------------------------

# Change sys.stdin so it provides universal newline support. 

sys.stdin = open(sys.stdin.fileno(), 'r', newline=None)


# ----------------------------------------------------------------------------------------------------------------------

_buffer = ''


# ----------------------------------------------------------------------------------------------------------------------

def writeln(x: object = ''):
    """
    Write x and an end-of-line mark to standard output.
    """
    x = str(x)
    sys.stdout.write(x)
    sys.stdout.write('\n')
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------------------------------

def write(x: object = ''):
    """
    Write x to standard output.
    """
    x = str(x)
    sys.stdout.write(x)
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------------------------------

def writef(fmt, *args):
    """
    Write each element of args to standard output.  Use the format specified by string fmt.
    """
    x = fmt % args
    sys.stdout.write(x)
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------------------------------

def _read_regular_expression(regular_expression):
    """
    Discard leading white space characters from standard input. Then read from standard input and return a string
    matching regular expression regular_expression.  Raise an EOFError if no non-whitespace characters remain in 
    standard input. Raise a ValueError if the next characters to be read from standard input do not match 
    'regular_expression'.
    """
    global _buffer
    if is_empty():
        raise EOFError()
    compiled_regular_expression = re.compile(r'^\s*' + regular_expression)
    match = compiled_regular_expression.search(_buffer)
    if match is None:
        raise ValueError()
    s = match.group()
    _buffer = _buffer[match.end():]
    return s.lstrip()


# ----------------------------------------------------------------------------------------------------------------------

def is_empty():
    """
    Return True if no non-whitespace characters remain in standard input. Otherwise return False.
    """
    global _buffer
    while _buffer.strip() == '':
        line = sys.stdin.readline()
        if line == '':
            return True
        _buffer += line
    return False


# ----------------------------------------------------------------------------------------------------------------------

def read_int():
    """
    Discard leading white space characters from standard input. Then read from standard input a sequence of characters
    comprising an integer. Convert the sequence of characters to an integer, and return the integer.  Raise an EOFError
    if no non-whitespace characters remain in standard input. Raise a ValueError if the next characters to be read from
    standard input cannot comprise an integer.
    """
    s = _read_regular_expression(r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)')
    radix = 10
    length = len(s)
    if (length >= 1) and (s[0:1] == '0'): 
        radix = 8
    if (length >= 2) and (s[0:2] == '-0'): 
        radix = 8
    if (length >= 2) and (s[0:2] == '0x'): 
        radix = 16
    if (length >= 2) and (s[0:2] == '0X'): 
        radix = 16
    if (length >= 3) and (s[0:3] == '-0x'): 
        radix = 16
    if (length >= 3) and (s[0:3] == '-0X'): 
        radix = 16
    return int(s, radix)


# ----------------------------------------------------------------------------------------------------------------------

def read_all_ints():
    """
    Read all remaining strings from standard input, convert each to an int, and return those ints in an array. Raise a
    ValueError if any of the strings cannot be converted to an int.
    """
    strings = read_all_strings()
    ints = []
    for s in strings:
        i = int(s)
        ints.append(i)
    return ints


# ----------------------------------------------------------------------------------------------------------------------

def read_float():
    """
    Discard leading white space characters from standard input. Then read from standard input a sequence of characters
    comprising a float. Convert the sequence of characters to a float, and return the float.  Raise an EOFError if no
    non-whitespace characters remain in standard input. Raise a ValueError if the next characters to be read from
    standard input cannot comprise a float.
    """
    s = _read_regular_expression(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
    return float(s)


# ----------------------------------------------------------------------------------------------------------------------

def read_all_floats():
    """
    Read all remaining strings from standard input, convert each to a float, and return those floats in an array. Raise
    a ValueError if any of the strings cannot be converted to a float.
    """
    strings = read_all_strings()
    floats = []
    for s in strings:
        f = float(s)
        floats.append(f)
    return floats


# ----------------------------------------------------------------------------------------------------------------------

def read_boolean():
    """
    Discard leading white space characters from standard input. Then read from standard input a sequence of characters
    comprising a bool. Convert the sequence of characters to a bool, and return the bool.  Raise an EOFError if no
    non-whitespace characters remain in standard input. Raise a ValueError if the next characters to be read from
    standard input cannot comprise a boolean.

    These character sequences can comprise a bool:
    -- True
    -- False
    -- 1 (means true)
    -- 0 (means false)
    """
    s = _read_regular_expression(r'(True)|(False)|1|0')
    if (s == 'True') or (s == '1'):
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------------

def read_all_booleans():
    """
    Read all remaining strings from standard input, convert each to a bool, and return those booleans in an array. Raise
    a ValueError if any of the strings cannot be converted to a boolean.
    """
    strings = read_all_strings()
    booleans = []
    for s in strings:
        b = bool(s)
        booleans.append(b)
    return booleans


# ----------------------------------------------------------------------------------------------------------------------

def read_string():
    """
    Discard leading white space characters from standard input. Then read from standard input a sequence of characters
    comprising a string, and return the string. Raise an EOFError if no non-whitespace characters remain in standard
    input.
    """
    s = _read_regular_expression(r'\S+')
    return s


# ----------------------------------------------------------------------------------------------------------------------

def read_all_strings():
    """
    Read all remaining strings from standard input, and return them in an array.
    """
    strings = []
    while not is_empty():
        s = read_string()
        strings.append(s)
    return strings


# ----------------------------------------------------------------------------------------------------------------------

def has_next_line():
    """
    Return True if standard input has a next line. Otherwise return False.
    """
    global _buffer
    if _buffer != '':
        return True
    else:
        _buffer = sys.stdin.readline()
        if _buffer == '':
            return False
        return True


# ----------------------------------------------------------------------------------------------------------------------

def read_line():
    """
    Read and return as a string the next line of standard input. Raise an EOFError is there is no next line.
    """
    global _buffer
    if not has_next_line():
        raise EOFError()
    s = _buffer
    _buffer = ''
    return s.rstrip('\n')


# ----------------------------------------------------------------------------------------------------------------------

def read_all_lines():
    """
    Read all remaining lines from standard input, and return them as strings in an array.
    """
    lines = []
    while has_next_line():
        line = read_line()
        lines.append(line)
    return lines


# ----------------------------------------------------------------------------------------------------------------------

def read_all():
    """
    Read and return as a string all remaining lines of standard input.
    """
    global _buffer
    s = _buffer
    _buffer = ''
    for line in sys.stdin:
        s += line
    return s


# ----------------------------------------------------------------------------------------------------------------------

def _test_write():
    writeln()
    writeln('string')
    writeln(123456)
    writeln(123.456)
    writeln(True)
    write()
    write('string')
    write(123456)
    write(123.456)
    write(True)
    writeln()
    writef('<%s> <%8d> <%14.8f>\n', 'string', 123456, 123.456)
    writef('formatstring\n')


# ----------------------------------------------------------------------------------------------------------------------

def _main():
    """
    For testing. The command-line argument should be the name of the
    function that should be called.
    """
    test_map = {
        'readInt':    read_int, 'readAllInts':    read_all_ints,
        'readFloat':  read_float, 'readAllFloats':  read_all_floats,
        'readBool':   read_boolean, 'readAllBools':   read_all_booleans,
        'readString': read_string, 'readAllStrings': read_all_strings,
        'readLine':   read_line, 'readAllLines':  read_all_lines,
        'readAll':    read_all
    }

    test_id = sys.argv[1]

    if test_id == 'write':
        _test_write()
    else:
        writeln(test_map[test_id]())


if __name__ == '__main__':
    _main()
