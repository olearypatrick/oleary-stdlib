"""
stddraw.py

The stddraw module defines functions that allow the user to create a drawing.  A drawing appears on the canvas.  The
canvas appears in the window.  As a convenience, the module also imports the commonly used Color objects defined in the
color module.
"""

import time
import os
import sys
import color
import tkinter
import tkinter.messagebox as tkmessagebox
import tkinter.filedialog as tkfiledialog

# ----------------------------------------------------------------------------------------------------------------------

# Define colors so clients need not import the color module.

from color import WHITE
from color import BLACK
from color import RED
from color import GREEN
from color import BLUE
from color import CYAN
from color import MAGENTA
from color import YELLOW
from color import DARK_RED
from color import DARK_GREEN
from color import DARK_BLUE
from color import ORANGE
from color import PINK

# ----------------------------------------------------------------------------------------------------------------------

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
import pygame.gfxdraw
import pygame.font


# ----------------------------------------------------------------------------------------------------------------------

# Default Sizes and Values

_BORDER = 0.0
_DEFAULT_X_MIN = 0.0
_DEFAULT_X_MAX = 1.0
_DEFAULT_Y_MIN = 0.0
_DEFAULT_Y_MAX = 1.0
_DEFAULT_CANVAS_SIZE = 512
_DEFAULT_PEN_RADIUS = .005
_DEFAULT_PEN_COLOR = color.BLACK

_DEFAULT_FONT_FAMILY = 'Helvetica'
_DEFAULT_FONT_SIZE = 12

_x_min = float(_DEFAULT_X_MIN)
_y_min = float(_DEFAULT_Y_MIN)
_x_max = float(_DEFAULT_X_MAX)
_y_max = float(_DEFAULT_Y_MAX)

_font_family = _DEFAULT_FONT_FAMILY
_font_size = _DEFAULT_FONT_SIZE

_background = None
_surface = None
_canvas_width = float(_DEFAULT_CANVAS_SIZE)
_canvas_height = float(_DEFAULT_CANVAS_SIZE)
_pen_radius = float(_DEFAULT_PEN_RADIUS)
_pen_color = _DEFAULT_PEN_COLOR
_keys_typed = []

_window_created = False

_mouse_pressed = False
_mouse_position = [0, 0]


# ----------------------------------------------------------------------------------------------------------------------

def _pygame_color(c):
    """
    Convert c, an object of type color.Color, to an equivalent object of type pygame.Color.  Return the result.
    """
    r = c.get_red()
    g = c.get_green()
    b = c.get_blue()
    return pygame.Color(r, g, b, 1)


# ----------------------------------------------------------------------------------------------------------------------

def _scale_x(x):
    return _canvas_width * (x - _x_min) / (_x_max - _x_min)


# ----------------------------------------------------------------------------------------------------------------------

def _scale_y(y):
    return _canvas_height * (_y_max - y) / (_y_max - _y_min)


# ----------------------------------------------------------------------------------------------------------------------

def _factor_x(w):
    return w * _canvas_width / abs(_x_max - _x_min)


# ----------------------------------------------------------------------------------------------------------------------

def _factor_y(h):
    return h * _canvas_height / abs(_y_max - _y_min)


# ----------------------------------------------------------------------------------------------------------------------

def _user_x(x):
    return _x_min + x * (_x_max - _x_min) / _canvas_width


# ----------------------------------------------------------------------------------------------------------------------

def _user_y(y):
    return _y_max - y * (_y_max - _y_min) / _canvas_height
    
    
# ----------------------------------------------------------------------------------------------------------------------

def set_canvas_size(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high. Calling this function is optional. If you call it,
    you must do so before calling any drawing function.
    """
    global _background
    global _surface
    global _canvas_width
    global _canvas_height
    global _window_created

    if _window_created:
        raise Exception('The stddraw window already was created')
    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')
    _canvas_width = w
    _canvas_height = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption('stddraw window (r-click to save)')
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygame_color(WHITE))
    _window_created = True


# ----------------------------------------------------------------------------------------------------------------------

def set_x_scale(_minimum=_DEFAULT_X_MIN, _maximum=_DEFAULT_X_MAX):
    """
    Set the x-scale of the canvas such that the minimum x value is min and the maximum x value is max.
    """
    global _x_min
    global _x_max

    minimum = float(_minimum)
    maximum = float(_maximum)
    if minimum >= maximum:
        raise Exception('minimum must be less than maximum')
    size = maximum - minimum
    _x_min = minimum - _BORDER * size
    _x_max = maximum + _BORDER * size


# ----------------------------------------------------------------------------------------------------------------------

def set_y_scale(_minimum=_DEFAULT_Y_MIN, _maximum=_DEFAULT_Y_MAX):
    """
    Set the y-scale of the canvas such that the minimum y value is min and the maximum y value is max.
    """
    global _y_min
    global _y_max

    minimum = float(_minimum)
    maximum = float(_maximum)
    if minimum >= maximum:
        raise Exception('minimum must be less than maximum')
    size = maximum - minimum
    _y_min = minimum - _BORDER * size
    _y_max = maximum + _BORDER * size


# ----------------------------------------------------------------------------------------------------------------------

def set_pen_radius(r=_DEFAULT_PEN_RADIUS):
    """
    Set the pen radius to r, thus affecting the subsequent drawing of points and lines. If r is 0.0, then points will be
    drawn with the minimum possible radius and lines with the minimum possible width.
    """
    global _pen_radius

    r = float(r)
    if r < 0.0:
        raise Exception('Argument to set_pen_radius() must be non-neg')
    _pen_radius = r * float(_DEFAULT_CANVAS_SIZE)


# ----------------------------------------------------------------------------------------------------------------------

def set_pen_color(c=_DEFAULT_PEN_COLOR):
    """
    Set the pen color to c, where c is an object of class color.Color. c defaults to stddraw.BLACK.
    """
    global _pen_color

    _pen_color = c


# ----------------------------------------------------------------------------------------------------------------------

def set_font_family(f=_DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _font_family

    _font_family = f


# ----------------------------------------------------------------------------------------------------------------------

def set_font_size(s=_DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _font_size

    _font_size = s


# ----------------------------------------------------------------------------------------------------------------------

def _make_sure_window_created():
    global _window_created

    if not _window_created:
        set_canvas_size()
        _window_created = True


# ----------------------------------------------------------------------------------------------------------------------

def _pixel(x, y):
    """
    Draw on the background canvas a pixel at (x, y).
    """
    _make_sure_window_created()
    xs = _scale_x(x)
    ys = _scale_y(y)
    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(ys)),
        _pygame_color(_pen_color))


# ----------------------------------------------------------------------------------------------------------------------

def point(x, y):
    """
    Draw on the background canvas a point at (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    if _pen_radius <= 1.0:
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(
                xs-_pen_radius,
                ys-_pen_radius,
                _pen_radius*2.0,
                _pen_radius*2.0),
            0)


# ----------------------------------------------------------------------------------------------------------------------

def _thick_line(x0, y0, x1, y1, r):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1). Draw the line with a pen whose radius is r.
    """
    xs0 = _scale_x(x0)
    ys0 = _scale_y(y0)
    xs1 = _scale_x(x1)
    ys1 = _scale_y(y1)
    if (abs(xs0-xs1) < 1.0) and (abs(ys0-ys1) < 1.0):
        filled_circle(x0, y0, r)
        return
    x_mid = (x0+x1)/2
    y_mid = (y0+y1)/2
    _thick_line(x0, y0, x_mid, y_mid, r)
    _thick_line(x_mid, y_mid, x1, y1, r)


# ----------------------------------------------------------------------------------------------------------------------

def line(x0, y0, x1, y1):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    """
    thick_line_cutoff = 3  # pixels
    _make_sure_window_created()
    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)
    line_width = _pen_radius * 2.0
    if line_width == 0.0: 
        line_width = 1.0
    if line_width < thick_line_cutoff:
        x0s = _scale_x(x0)
        y0s = _scale_y(y0)
        x1s = _scale_x(x1)
        y1s = _scale_y(y1)
        pygame.draw.line(
            _surface,
            _pygame_color(_pen_color),
            (x0s, y0s),
            (x1s, y1s),
            int(round(line_width)))
    else:
        _thick_line(x0, y0, x1, y1, _pen_radius / _DEFAULT_CANVAS_SIZE)


# ----------------------------------------------------------------------------------------------------------------------

def circle(x, y, r):
    """
    Draw on the background canvas a circle of radius r centered on (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factor_x(2.0 * r)
    hs = _factor_y(2.0 * r)
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(
                xs-ws/2.0, 
                ys-hs/2.0, 
                ws, 
                hs),
            int(round(_pen_radius)))


# ----------------------------------------------------------------------------------------------------------------------

def filled_circle(x, y, r):
    """
    Draw on the background canvas a filled circle of radius r centered on (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factor_x(2.0 * r)
    hs = _factor_y(2.0 * r)
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(
                xs-ws/2.0, 
                ys-hs/2.0, 
                ws, 
                hs),
            0)


# ----------------------------------------------------------------------------------------------------------------------

def rectangle(x, y, w, h):
    """
    Draw on the background canvas a rectangle of width w and height h whose lower left point is (x, y).
    """
    global _surface

    _make_sure_window_created()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factor_x(w)
    hs = _factor_y(h)
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.rect(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(
                xs, 
                ys-hs, 
                ws, 
                hs),
            int(round(_pen_radius)))


# ----------------------------------------------------------------------------------------------------------------------

def filled_rectangle(x, y, w, h):
    """
    Draw on the background canvas a filled rectangle of width w and height h whose lower left point is (x, y).
    """
    global _surface

    _make_sure_window_created()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factor_x(w)
    hs = _factor_y(h)
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.rect(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(
                xs, 
                ys-hs, 
                ws, 
                hs),
            0)


# ----------------------------------------------------------------------------------------------------------------------

def square(x, y, r):
    """
    Draw on the background canvas a square whose sides are of length 2r, centered on (x, y).
    """
    _make_sure_window_created()
    rectangle(x-r, y-r, 2.0*r, 2.0*r)


# ----------------------------------------------------------------------------------------------------------------------

def filled_square(x, y, r):
    """
    Draw on the background canvas a filled square whose sides are of length 2r, centered on (x, y).
    """
    _make_sure_window_created()
    filled_rectangle(x-r, y-r, 2.0*r, 2.0*r)


# ----------------------------------------------------------------------------------------------------------------------

def polygon(x, y):
    """
    Draw on the background canvas a polygon with coordinates (x[i], y[i]).
    """
    global _surface

    _make_sure_window_created()
    x_scaled = []
    for xi in x:
        x_scaled.append(_scale_x(float(xi)))
    y_scaled = []
    for yi in y:
        y_scaled.append(_scale_y(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((x_scaled[i], y_scaled[i]))
    points.append((x_scaled[0], y_scaled[0]))
    pygame.draw.polygon(
        _surface,
        _pygame_color(_pen_color),
        points,
        int(round(_pen_radius)))


# ----------------------------------------------------------------------------------------------------------------------

def filled_polygon(x, y):
    """
    Draw on the background canvas a filled polygon with coordinates (x[i], y[i]).
    """
    global _surface

    _make_sure_window_created()
    x_scaled = []
    for xi in x:
        x_scaled.append(_scale_x(float(xi)))
    y_scaled = []
    for yi in y:
        y_scaled.append(_scale_y(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((x_scaled[i], y_scaled[i]))
    points.append((x_scaled[0], y_scaled[0]))
    pygame.draw.polygon(
        _surface,
        _pygame_color(_pen_color),
        points,
        0)


# ----------------------------------------------------------------------------------------------------------------------

def text(x, y, s):
    """
    Draw string s on the background canvas centered at (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    xs = _scale_x(x)
    ys = _scale_y(y)
    font = pygame.font.SysFont(_font_family, _font_size)
    font_render = font.render(s, 1, _pygame_color(_pen_color))
    text_position = font_render.get_rect(center=(xs, ys))
    _surface.blit(font_render, text_position)


# ----------------------------------------------------------------------------------------------------------------------

def picture(_picture, x=None, y=None):
    """
    Draw pic on the background canvas centered at (x, y).  pic is an object of class picture.Picture. x and y default to
    the midpoint of the background canvas.
    """
    global _surface

    _make_sure_window_created()
    if x is None:
        x = (_x_max + _x_min) / 2.0
    if y is None:
        y = (_y_max + _y_min) / 2.0
    x = float(x)
    y = float(y)
    xs = _scale_x(x)
    ys = _scale_y(y)
    ws = _picture.width()
    hs = _picture.height()
    picture_surface = _picture._surface
    _surface.blit(picture_surface, [xs-ws/2.0, ys-hs/2.0, ws, hs])


# ----------------------------------------------------------------------------------------------------------------------

def clear(c=WHITE):
    """
    Clear the background canvas to color c, where c is an object of class color.Color. c defaults to stddraw.WHITE.
    """
    _make_sure_window_created()
    _surface.fill(_pygame_color(c))


# ----------------------------------------------------------------------------------------------------------------------

def save(f):
    """
    Save the window canvas to file f.
    """
    _make_sure_window_created()
    pygame.image.save(_surface, f)


# ----------------------------------------------------------------------------------------------------------------------

def _show():
    """
    Copy the background canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    _check_for_events()


# ----------------------------------------------------------------------------------------------------------------------

def _show_and_wait_forever():
    """
    Copy the background canvas to the window canvas. Then wait forever, that is, until the user closes the stddraw
    window.
    """
    _make_sure_window_created()
    _show()
    quantum = .1
    while True:
        time.sleep(quantum)
        _check_for_events()


# ----------------------------------------------------------------------------------------------------------------------

def show(m_second=float('inf')):
    """
    Copy the background canvas to the window canvas, and then wait for msec milliseconds. msec defaults to infinity.
    """
    if m_second == float('inf'):
        _show_and_wait_forever()
    _make_sure_window_created()
    _show()
    _check_for_events()
    quantum = .1
    second = m_second / 1000.0
    if second < quantum:
        time.sleep(second)
        return
    seconds_waited = 0.0
    while seconds_waited < second:
        time.sleep(quantum)
        seconds_waited += quantum
        _check_for_events()


# ----------------------------------------------------------------------------------------------------------------------

def _save_to_file():
    """
    Display a dialog box that asks the user for a file name.  Save the drawing to the specified file.  Display a
    confirmation dialog box if successful, and an error dialog box otherwise.  The dialog boxes are displayed using
    tkinter, which (on some computers) is incompatible with Pygame. So the dialog boxes must be displayed from child
    processes.
    """
    import subprocess

    _make_sure_window_created()
    _stddraw_path = os.path.realpath(__file__)
    _child_process = subprocess.Popen(
        [sys.executable, _stddraw_path, 'getFileName'],
        stdout=subprocess.PIPE)
    so, se = _child_process.communicate()
    filename = so.strip()
    filename = filename.decode('utf-8')
    if filename == '':
        return
    if not filename.endswith(('.jpg', '.png')):
        _child_process = subprocess.Popen(
            [sys.executable, _stddraw_path,
             'reportFileSaveError',
             'File name must end with ".jpg" or ".png".'])
        return
    try:
        save(filename)
        _child_process = subprocess.Popen(
            [sys.executable, _stddraw_path, 'confirmFileSave'])
    except pygame.error as e:
        _child_process = subprocess.Popen(
            [sys.executable, _stddraw_path, 'reportFileSaveError', str(e)])


# ----------------------------------------------------------------------------------------------------------------------

def _check_for_events():
    """
    Check if any new event has occured (such as a key typed or button pressed).  If a key has been typed, then put that
    key in a queue.
    """
    global _surface
    global _keys_typed
    global _mouse_position
    global _mouse_pressed
    
    _make_sure_window_created()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keys_typed = [event.unicode] + _keys_typed
        elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 3):
            _save_to_file()
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            _mouse_pressed = True
            _mouse_position = event.pos


# ----------------------------------------------------------------------------------------------------------------------

def has_next_key_typed():
    """
    Return True if the queue of keys the user typed is not empty. Otherwise return False.
    """
    global _keys_typed

    return _keys_typed != []


# ----------------------------------------------------------------------------------------------------------------------

def next_key_typed():
    """
    Remove the first key from the queue of keys that the the user typed, and return that key.
    """
    global _keys_typed

    return _keys_typed.pop()


# ----------------------------------------------------------------------------------------------------------------------

def mouse_pressed():
    """
    Return True if the mouse has been left-clicked since the last time mousePressed was called, and False otherwise.
    """
    global _mouse_pressed

    if _mouse_pressed:
        _mouse_pressed = False
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------------

def mouse_x():
    """
    Return the x coordinate in user space of the location at which the mouse was most recently left-clicked. If a
    left-click hasn't happened yet, raise an exception, since mouseX() shouldn't be called until mousePressed() returns
    True.
    """
    global _mouse_position

    if _mouse_position:
        return _user_x(_mouse_position[0])      
    raise Exception("Can't determine mouse position if a click hasn't happened")


# ----------------------------------------------------------------------------------------------------------------------

def mouse_y():
    """
    Return the y coordinate in user space of the location at which the mouse was most recently left-clicked. If a
    left-click hasn't happened yet, raise an exception, since mouseY() shouldn't be called until mousePressed() returns
    True.
    """
    global _mouse_position

    if _mouse_position:
        return _user_y(_mouse_position[1]) 
    raise Exception("Can't determine mouse position if a click hasn't happened")


# ----------------------------------------------------------------------------------------------------------------------

def _get_filename():
    """
    Display a dialog box that asks the user for a file name.
    """
    root = tkinter.Tk()
    root.withdraw()
    reply = tkfiledialog.asksaveasfilename(initialdir='.')
    sys.stdout.write(reply)
    sys.stdout.flush()
    sys.exit()


# ----------------------------------------------------------------------------------------------------------------------

def _confirm_file_save():
    """
    Display a dialog box that confirms a file save operation.
    """
    root = tkinter.Tk()
    root.withdraw()
    tkmessagebox.showinfo(
        title='File Save Confirmation',
        message='The drawing was saved to the file.')
    sys.exit()


# ----------------------------------------------------------------------------------------------------------------------

def _report_file_save_error(msg):
    """
    Display a dialog box that reports a msg.  msg is a string which
    describes an error in a file save operation.
    """
    root = tkinter.Tk()
    root.withdraw()
    tkmessagebox.showerror(
        title='File Save Error',
        message=msg)
    sys.exit()


# ----------------------------------------------------------------------------------------------------------------------

# Initialize the x scale, the y scale, the pen radius, and the pygame font system.

set_x_scale()
set_y_scale()
set_pen_radius()
pygame.font.init()


# ----------------------------------------------------------------------------------------------------------------------

def _regression_test():
    """
    Perform regression testing.
    """

    clear()

    set_pen_radius(.5)
    set_pen_color(ORANGE)
    point(0.5, 0.5)
    show(0.0)

    set_pen_radius(.25)
    set_pen_color(BLUE)
    point(0.5, 0.5)
    show(0.0)

    set_pen_radius(.02)
    set_pen_color(RED)
    point(0.25, 0.25)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(GREEN)
    point(0.25, 0.25)
    show(0.0)

    set_pen_radius(0)
    set_pen_color(BLACK)
    point(0.25, 0.25)
    show(0.0)

    set_pen_radius(.1)
    set_pen_color(RED)
    point(0.75, 0.75)
    show(0.0)

    set_pen_radius(0)
    set_pen_color(CYAN)
    for i in range(0, 100):
        point(i / 512.0, .5)
        point(.5, i / 512.0)
    show(0.0)

    set_pen_radius(0)
    set_pen_color(MAGENTA)
    line(.1, .1, .3, .3)
    line(.1, .2, .3, .2)
    line(.2, .1, .2, .3)
    show(0.0)

    set_pen_radius(.05)
    set_pen_color(MAGENTA)
    line(.7, .5, .8, .9)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(YELLOW)
    circle(.75, .25, .2)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(YELLOW)
    filled_circle(.75, .25, .1)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(PINK)
    rectangle(.25, .75, .1, .2)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(PINK)
    filled_rectangle(.25, .75, .05, .1)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(DARK_RED)
    square(.5, .5, .1)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(DARK_RED)
    filled_square(.5, .5, .05)
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(DARK_BLUE)
    polygon([.4, .5, .6], [.7, .8, .7])
    show(0.0)

    set_pen_radius(.01)
    set_pen_color(DARK_GREEN)
    set_font_size(24)
    text(.2, .4, 'hello, world')
    show(0.0)

    import picture as p

    pic = p.Picture('saveIcon.png')
    picture(pic, .5, .85)
    show(0.0)
    
    set_pen_color(BLACK)
    import stdio

    stdio.writeln('Left click with the mouse or type a key')
    while True:
        if mouse_pressed():
            filled_circle(mouse_x(), mouse_y(), .02)
        if has_next_key_typed():
            stdio.write(next_key_typed())
        show(0.0)


# ----------------------------------------------------------------------------------------------------------------------

def _main():
    """
    Dispatch to a function that does regression testing, or to a dialog-box-handling function.
    """
    import sys
    if len(sys.argv) == 1:
        _regression_test()
    elif sys.argv[1] == 'getFileName':
        _get_filename()
    elif sys.argv[1] == 'confirmFileSave':
        _confirm_file_save()
    elif sys.argv[1] == 'reportFileSaveError':
        _report_file_save_error(sys.argv[2])


if __name__ == '__main__':
    _main()
