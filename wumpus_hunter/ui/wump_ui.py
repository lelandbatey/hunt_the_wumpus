from __future__ import print_function
import os.path
import base64
import random
import time
import json
import os

# Done to allow the importing of graphics.py
import sys
sys.path.append('../')
import graphics as gfx


def get_image(image_path, force=False):
    """Loads a gif image as a base64 string.

    If just a filename is passed without any path info, then it is assumed the
    given file names in the `./images/` directory. This behaviour can be
    turned off via the 'force' variable."""

    path_parts = os.path.split(image_path)

    if len(path_parts) < 2 and not force:
        image_path = os.path.join(['images'] + path_parts)

    with open(image_path, 'r') as img:
        filestr = base64.encodestring(img.read())
    return filestr


# Written by Russel Swannack
# Used with permission.
def get_rect_intersect(my_rectangle, my_point):
    """Given a rectangle and point, check if the point is in the rectangle."""
    # Need to account for the possibility that the rectangle was constructed
    # backwards
    pnt_1x = min(my_rectangle.getP1().getX(), my_rectangle.getP2().getX())
    pnt_2x = max(my_rectangle.getP1().getX(), my_rectangle.getP2().getX())
    pnt_1y = min(my_rectangle.getP1().getY(), my_rectangle.getP2().getY())
    pnt_2y = max(my_rectangle.getP1().getY(), my_rectangle.getP2().getY())

    # Get Test Point Info
    test_pnt_x, test_pnt_y = my_point.getX(), my_point.getY()

    # Check to see if the test point is within the rectangle bounds
    is_within = test_pnt_x >= pnt_1x \
    and test_pnt_x <= pnt_2x \
    and test_pnt_y >= pnt_1y \
    and test_pnt_y <= pnt_2y

    return is_within


def which_button(click, button_dict):
    """Checks which rectangle a point falls in for a dict of rectangles.

    Returns the key of the entry in the dict that the point falls within, or
    `None` if the point is not within any of the rectangles.
    """

    for key in button_dict:
        if get_rect_intersect(button_dict[key], click):
            return key
    # This could be left out and the return None left implicit, but that seems
    # like it could be confusing.
    return None


def make_buttons(btn_sttings):
    """Converts a json-stle structure into dict of rectangles."""
    buttons = {}
    for key in btn_sttings:
        pnt1, pnt2 = btn_sttings[key]
        buttons[key] = gfx.Rectangle(gfx.Point(pnt1), gfx.Point(pnt2))
    return buttons


class Window(object):
    """A re-usable window object.

    Since there's just a ton of different little variables that need to be set
    for a window to work properly, I figure I can easily defer all that into
    some configuration files, then just monitor which buttons get clicked.

    """

    def __init__(self, settings):
        if isinstance(settings, basestring):
            settings = json.load(
                open(os.path.join(['layout', settings + '.json'])))
        self.settings = settings
        self.window = gfx.GraphWin(self.settings['title'],
                                   self.settings['width'],
                                   self.settings['height'])

        self.buttons = make_buttons(settings['buttons'])

    def place_buttons(self):
        """Draws the buttons onto the window."""
        pass

    def get_buttonclick(self):
        """Waits for the user to click a button.

        If the user instead closes the window, then the button variable is
        unset and the failure variable is set to True.
        """

        done = False
        button, failure = None, None
        while not done:
            # Try is for user clicking the close button.
            try:
                click = self.window.getMouse()
            except GraphicsError:
                failure = True
                button = None
            # Wait for a user to click inside a button
            if not done:
                # I don't want names of variables to be subsets of each other
                clkd = which_button(click, self.buttons)
                if clkd is not None:
                    failure = False
                    button = clkd
                    done = True
        self.window.close()
        return button, failure


class DifficultyWindow(object):
    """Controls getting the difficulty from the user."""

    def __init__(self):
        self.window = gfx.GraphWin("Choose the Difficulty", 400, 100)
        self.buttons = {}
        self.place_buttons()
        self.difficulty, self.failure = self.get_difficulty()

    def place_buttons(self):
        """Places various buttons on the board."""
        # Saving these rectangles allows us to check if a click falls inside a
        # button later.
        buttons = {
            'easy': gfx.Rectangle(gfx.Point(66, 36), gfx.Point(134, 64)),
            'medium': gfx.Rectangle(gfx.Point(166, 36), gfx.Point(234, 64)),
            'hard': gfx.Rectangle(gfx.Point(266, 36), gfx.Point(334, 64))
        }
        self.buttons = buttons

        # Draw each button
        button_points = [[100, 50], [200, 50], [300, 50]]
        bnames = ["easybutton.gif", 'mediumbutton.gif', 'hardbutton.gif']
        for index, point in enumerate(button_points):
            gfx.Image(gfx.Point(point), {
                'data': get_image(bnames[index])
            }).draw(self.window)

    def get_difficulty(self):
        """Waits for the user to click a difficulty.

        If the user instead closes the window, then the difficulty variable is
        unset and the failure variable is set to True.
        """

        done = False
        difficulty, failure = None, None
        while not done:
            # Try is for user clicking the close button.
            try:
                click = self.window.getMouse()
            except GraphicsError:
                failure = True
                difficulty = None
            # Wait for a user to click inside a button
            if not done:
                # I don't want names of variables to be subsets of each other
                clkd = which_button(click, self.buttons)
                if clkd is not None:
                    failure = False
                    difficulty = clkd
                    done = True
        self.window.close()
        return difficulty, failure
