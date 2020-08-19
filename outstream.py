"""
outstream.py

The outstream module defines the OutStream class.
"""

import sys


# ----------------------------------------------------------------------------------------------------------------------

class OutStream:

    """
    An OutStream object wraps around a text file or sys.stdout, and
    supports writing to that stream.
    """

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, f=None):
        """
        Construct self to wrap around a stream. If f is provided, then the stream is a file of that name.  Otherwise the
        stream is standard output.
        """
        if f is None:
            self._stream = sys.stdout
        else:
            self._stream = open(f, 'w', encoding='utf-8')

    # ------------------------------------------------------------------------------------------------------------------

    def writeln(self, x=''):
        """
        Write x and an end-of-line mark to the stream wrapped by self.
        """
        x = str(x)
        self._stream.write(x)
        self._stream.write('\n')
        self._stream.flush()

    # ------------------------------------------------------------------------------------------------------------------

    def write(self, x=''):
        """
        Write x to the stream wrapped by self.
        """
        x = str(x)
        self._stream.write(x)
        self._stream.flush()

    # ------------------------------------------------------------------------------------------------------------------

    def writef(self, fmt, *args):
        """
        Write each element of args to the stream wrapped by self. Use the format specified by string fmt.
        """
        x = fmt % args
        self._stream.write(x)
        self._stream.flush()

    # ------------------------------------------------------------------------------------------------------------------

    def __del__(self):
        """
        Close the stream wrapped by self.
        """
        self._stream.close()
