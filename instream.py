"""
instream.py

The instream module defines the InStream class.
"""

import sys
import urllib.request as urllib
import re


# ----------------------------------------------------------------------------------------------------------------------

class InStream:
    """
    An InStream object wraps around a text file or sys.stdin, and supports reading from that stream.
    """

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_or_url=None):
        """
        Construct self to wrap around a stream. The stream can be a file whose name is given as file_or_url, a resource
        whose URL is given as file_or_url, or sys.stdin by default.
        """
        self._buffer = ''
        self._stream = None
        self._reading_web_page = False
        if file_or_url is None:
            import stdio  # To change the mode of sys.stdin
            self._stream = sys.stdin
            return
        try:
            self._stream = open(file_or_url, 'r', encoding='utf-8')  # Try to open a file
        except IOError:
            try:
                self._stream = urllib.urlopen(file_or_url)  # Try to open a URL
                self._reading_web_page = True
            except IOError:
                raise IOError('No such file or URL: ' + file_or_url)

    # ------------------------------------------------------------------------------------------------------------------

    def _read_regular_expression(self, regular_expression):
        """
        Discard leading white space characters from the stream wrapped by self.  Then read from the stream and return a
        string matching regular expression regular_expression.  Raise an EOFError if no non-whitespace characters remain
        in the stream. Raise a ValueError if the next characters to be read from the stream do not match 
        regular_expression.
        """
        if self.is_empty():
            raise EOFError()
        compiled_regular_expression = re.compile(r'^\s*' + regular_expression)
        match = compiled_regular_expression.search(self._buffer)
        if match is None:
            raise ValueError()
        s = match.group()
        self._buffer = self._buffer[match.end():]
        return s.lstrip()

    # ------------------------------------------------------------------------------------------------------------------

    def is_empty(self):
        """
        Return True if no non-whitespace characters remain in the stream wrapped by self.
        """
        while self._buffer.strip() == '':
            line = self._stream.readline()
            if line == '':
                return True
            self._buffer += str(line)
        return False

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def read_int(self):
        """
        Discard leading white space characters from the stream wrapped by self.  Then read from the stream a sequence of
        characters comprising an integer.  Convert the sequence of characters to an integer, and return the integer.
        Raise an EOFError if no non-whitespace characters remain in the stream.  Raise a ValueError if the next
        characters to be read from the stream cannot comprise an integer.
        """
        s = self._read_regular_expression(r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)')
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

    # ------------------------------------------------------------------------------------------------------------------

    def read_all_ints(self):
        """
        Read all remaining strings from the stream wrapped by self, convert  each to an int, and return those ints in an
        array. Raise a ValueError if any of the strings cannot be converted to an int.
        """
        strings = self.read_all_strings()
        ints = []
        for s in strings:
            i = int(s)
            ints.append(i)
        return ints

    # ------------------------------------------------------------------------------------------------------------------

    def read_float(self):
        """
        Discard leading white space characters from the stream wrapped by self.  Then read from the stream a sequence of
        characters comprising a float.  Convert the sequence of characters to an float, and return the float.  Raise an
        EOFError if no non-whitespace characters remain in the stream.  Raise a ValueError if the next characters to be
        read from the stream cannot comprise a float.
        """
        s = self._read_regular_expression(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
        return float(s)

    # ------------------------------------------------------------------------------------------------------------------

    def read_all_floats(self):
        """
        Read all remaining strings from the stream wrapped by self, convert each to a float, and return those floats in
        an array. Raise a ValueError if any of the strings cannot be converted to a float.
        """
        strings = self.read_all_strings()
        floats = []
        for s in strings:
            f = float(s)
            floats.append(f)
        return floats

    # ------------------------------------------------------------------------------------------------------------------

    def read_boolean(self):
        """
        Discard leading white space characters from the stream wrapped by self.  Then read from the stream a sequence of
        characters comprising a bool.  Convert the sequence of characters to an bool, and return the bool.  Raise an
        EOFError if no non-whitespace characters remain in the stream.  Raise a ValueError if the next characters to be
        read from the stream cannot comprise an bool.
        """
        s = self._read_regular_expression(r'(True)|(False)|1|0')
        if (s == 'True') or (s == '1'):
            return True
        return False

    # ------------------------------------------------------------------------------------------------------------------

    def read_all_booleans(self):
        """
        Read all remaining strings from the stream wrapped by self, convert each to a bool, and return those 
        booleans in an array. Raise a ValueError if any of the strings cannot be converted to a boolean.
        """
        strings = self.read_all_strings()
        booleans = []
        for s in strings:
            b = bool(s)
            booleans.append(b)
        return booleans

    # ------------------------------------------------------------------------------------------------------------------

    def read_string(self):
        """
        Discard leading white space characters from the stream wrapped by self.  Then read from the stream a sequence of
        characters comprising a string, and return the string. Raise an EOFError if no non-whitespace characters remain 
        in the stream.
        """
        s = self._read_regular_expression(r'\S+')
        return s

    # ------------------------------------------------------------------------------------------------------------------

    def read_all_strings(self):
        """
        Read all remaining strings from the stream wrapped by self, and return them in an array.
        """
        strings = []
        while not self.is_empty():
            s = self.read_string()
            strings.append(s)
        return strings

    # ------------------------------------------------------------------------------------------------------------------

    def has_next_line(self):
        """
        Return True iff the stream wrapped by self has a next line.
        """
        if self._buffer != '':
            return True
        else:
            self._buffer = self._stream.readline()
            if self._buffer == '':
                return False
            return True

    # ------------------------------------------------------------------------------------------------------------------

    def read_line(self):
        """
        Read and return as a string the next line of the stream wrapped by self.  Raise an EOFError is there is no next 
        line.
        """
        if not self.has_next_line():
            raise EOFError()
        s = self._buffer
        self._buffer = ''
        return s.rstrip('\n')

    # ------------------------------------------------------------------------------------------------------------------

    def read_all_lines(self):
        """
        Read all remaining lines from the stream wrapped by self, and return them as strings in an array.
        """
        lines = []
        while self.has_next_line():
            line = self.read_line()
            lines.append(line)
        return lines

    # ------------------------------------------------------------------------------------------------------------------

    def read_all(self):
        """
        Read and return as a string all remaining lines of the stream wrapped by self.
        """
        s = self._buffer
        self._buffer = ''
        for line in self._stream:
            if self._reading_web_page:
                line = line.decode('utf-8')
            s += line
        return s

    # ------------------------------------------------------------------------------------------------------------------

    def __del__(self):
        """
        Close the stream wrapped by self.
        """
        if self._stream is not None:
            self._stream.close()


# ----------------------------------------------------------------------------------------------------------------------

def _main():
    """
    For testing. The first command-line argument should be the name of the method that should be called. The optional 
    second command-line argument should be the file or URL to read.
    """

    import stdio

    test_id = sys.argv[1]
    if len(sys.argv) > 2:
        instream = InStream(sys.argv[2])
    else:
        instream = InStream()

    if test_id == 'read_int':
        stdio.writeln(instream.read_int)
    elif test_id == 'read_all_ints':
        stdio.writeln(instream.read_all_ints())
    elif test_id == 'read_float':
        stdio.writeln(instream.read_float())
    elif test_id == 'read_all_floats':
        stdio.writeln(instream.read_all_floats())
    elif test_id == 'read_boolean':
        stdio.writeln(instream.read_boolean())
    elif test_id == 'read_all_booleans':
        stdio.writeln(instream.read_all_booleans())
    elif test_id == 'read_string':
        stdio.writeln(instream.read_string())
    elif test_id == 'read_all_strings':
        stdio.writeln(instream.read_all_strings())
    elif test_id == 'read_line':
        stdio.writeln(instream.read_line())
    elif test_id == 'read_all_lines':
        stdio.writeln(instream.read_all_lines())
    elif test_id == 'read_all':
        stdio.writeln(instream.read_all())


if __name__ == '__main__':
    _main()
