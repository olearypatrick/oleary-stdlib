"""
picture.py

The picture module defines the Picture class.
"""

import os
import color

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# ----------------------------------------------------------------------------------------------------------------------

_DEFAULT_WIDTH = 512
_DEFAULT_HEIGHT = 512


# ----------------------------------------------------------------------------------------------------------------------

class Picture:
    """
    A Picture object models an image.  It is initialized such that it has a given width and height and contains all
    black pixels. Subsequently you can load an image from a given JPG or PNG file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, arg1=None, arg2=None):
        """
        If both arg1 and arg2 are None, then construct self such that it is all black with _DEFAULT_WIDTH and height
        _DEFAULT_HEIGHT. If arg1 is not None and arg2 is None, then construct self by reading from the file whose name
        is arg1. If neither arg1 nor arg2 is None, then construct self such that it is all black with width arg1 and and
        height arg2.
        """
        if (arg1 is None) and (arg2 is None):
            max_w = _DEFAULT_WIDTH
            max_h = _DEFAULT_HEIGHT
            self._surface = pygame.Surface((max_w, max_h))
            self._surface.fill((0, 0, 0))
        elif (arg1 is not None) and (arg2 is None):
            filename = arg1
            try:
                self._surface = pygame.image.load(filename)
            except pygame.error:
                raise IOError()
        elif (arg1 is not None) and (arg2 is not None):
            max_w = arg1
            max_h = arg2
            self._surface = pygame.Surface((max_w, max_h))
            self._surface.fill((0, 0, 0))
        else:
            raise ValueError()

    # ------------------------------------------------------------------------------------------------------------------

    def save(self, f):
        """
        Save self to the file whose name is f.
        """
        pygame.image.save(self._surface, f)

    # ------------------------------------------------------------------------------------------------------------------

    def width(self):
        """
        Return the width of self.
        """
        return self._surface.get_width()

    # ------------------------------------------------------------------------------------------------------------------

    def height(self):
        """
        Return the height of self.
        """
        return self._surface.get_height()

    # ------------------------------------------------------------------------------------------------------------------

    def get(self, x, y):
        """
        Return the color of self at location (x, y).
        """
        pygame_color = self._surface.get_at((x, y))
        return color.Color(pygame_color.r, pygame_color.g, pygame_color.b)

    # ------------------------------------------------------------------------------------------------------------------

    def set(self, x, y, c):
        """
        Set the color of self at location (x, y) to c.
        """
        pygame_color = pygame.Color(c.get_red(), c.get_green(), c.get_blue(), 0)
        self._surface.set_at((x, y), pygame_color)
