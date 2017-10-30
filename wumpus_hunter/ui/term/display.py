"""
"""

import logging
import curses

from . import curses_colors
# cell['contents'] is a character representing its contents. Changing
# the color is done under rv.attr = ...


def get_colorpair(pair_name):
    val = curses_colors.CURSES_COLORPAIRS[pair_name]
    return curses.color_pair(val)


def left_edge(cell, width, height):
    return cell['x'] == 0


def right_edge(cell, width, height):
    return cell['x'] == width - 1


def top_edge(cell, width, height):
    return cell['y'] == 0


def bottom_edge(cell, width, height):
    return cell['y'] == height - 1


class Glyph(object):
    """
    Class Glyph contains data for a single symbol or unit which shall be drawn
    to a curses window.
    """

    def __init__(self, x, y, strng):
        self.x = x
        self.y = y
        self.strng = strng
        self.attr = get_colorpair('white-black')

    def __str__(self):
        return self.strng

    def __repr__(self):
        return str(self.__dict__)


def _upleft(cx, cy, cell, width, height):
    x, y = cx - 1, cy - 1
    if top_edge(cell, width, height):
        if left_edge(cell, width, height):
            return Glyph(x, y, "┌")
        else:
            return Glyph(x, y, "┬")
    else:
        if left_edge(cell, width, height):
            return Glyph(x, y, "├")
        else:
            return Glyph(x, y, "┼")


def _downleft(cx, cy, cell, width, height):
    x, y, = cx - 1, cy + 1
    if bottom_edge(cell, width, height):
        if left_edge(cell, width, height):
            return Glyph(x, y, "└")
        else:
            return Glyph(x, y, "┴")
    else:
        if left_edge(cell, width, height):
            return Glyph(x, y, "├")
        else:
            return Glyph(x, y, "┼")


def _upright(cx, cy, cell, width, height):
    x, y = cx + len(cell['contents']), cy - 1
    if top_edge(cell, width, height):
        if right_edge(cell, width, height):
            return Glyph(x, y, "┐")
        else:
            return Glyph(x, y, "┬")
    else:
        if right_edge(cell, width, height):
            return Glyph(x, y, "┤")
        else:
            return Glyph(x, y, "┼")


def _downright(cx, cy, cell, width, height):
    x, y = cx + len(cell['contents']), cy + 1
    if bottom_edge(cell, width, height):
        if right_edge(cell, width, height):
            return Glyph(x, y, "┘")
        else:
            return Glyph(x, y, "┴")
    else:
        if right_edge(cell, width, height):
            return Glyph(x, y, "┤")
        else:
            return Glyph(x, y, "┼")


def build_contents(cell):
    """
    Function build_contents returns a Glyph representing the contents of a
    cell, based on the state of that cell
    """
    x = ((1 + len(cell['contents'])) * cell['x']) + 1
    y = (2 * cell['y']) + 1
    rv = Glyph(x, y, cell['contents'])
    # color cell white on black
    rv.attr = get_colorpair('black-white')
    # rv.strng = " {} ".format(<whatever>)
    return rv


def assemble_glyphs(cell, width, height):
    cwidth = len(cell['contents'])
    # Starting cell position is:
    #     ((length_in_dimension+1)*n) + 1
    # ypos = lambda y: (2*y)+1
    # xpos = lambda x: ((1+cwidth)*x)+1

    # The x position on the curses field where the glyph will be drawn
    x = ((1 + cwidth) * cell['x']) + 1
    y = (2 * cell['y']) + 1

    contents_glyph = build_contents(cell)

    borders = [
        # Top border
        Glyph(x, y + 1, "─" * cwidth),
        # Bottom border
        Glyph(x, y - 1, "─" * cwidth),
        # Left and right
        Glyph(x - 1, y, "│"),
        Glyph(x + cwidth, y, "│"),
    ]
    corners = [func(x, y, cell, width, height)
               for func in (_upleft, _upright, _downright, _downleft)]
    rv = borders + corners + [contents_glyph]
    return rv
