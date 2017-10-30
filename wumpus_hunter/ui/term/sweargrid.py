"""
Easily display gameboard grid in terminal
"""
import logging
import curses
import queue
import threading

import time
import sys

from . import curses_colors, display
from .concurrency import concurrent

DEBUG = False

def input_reader(run_event, outqueue, resize_notify_queue, get_input):
    """
    wait for user input from curses, then place that input into
    outqueue. If terminal-resize event is detected, do not place in
    outqueue. Instead, send resize-event notification to the main
    terminal-drawing queue
    """
    while run_event.is_set():
        char = get_input()
        if char == curses.KEY_RESIZE:
            resize_notify_queue.put(('terminal resized', None))
            continue
        outqueue.put(char)


def grid_to_terminal_size(grid_width, grid_height):
    '''
    Return the height and width of a grid of characters needed to
    display a board with the given input dimensions.
    '''
    cwidth = 3
    termwidth = ((cwidth + 1) * board_width) + 1
    termheight = (board_height * 2) + 1
    return termwidth, termheight


class FakeStdscr(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.par_height, self.par_width = stdscr.getmaxyx()
        self.pad = curses.newpad(self.par_height + 200, self.par_width + 200)
        # Tells curses to leave key sequences from keypads in the input stream
        # and allows us to read them.
        self.pad.keypad(1)
        self.startx = 1
        self.starty = 1

    def refresh(self):
        # Reset the parent height on each refresh, to allow proper redrawing on
        # terminal resize
        self.par_height, self.par_width = self.stdscr.getmaxyx()
        self.pad.refresh(0, 0, 0, 0, self.par_height - 1, self.par_width - 1)

    def getmaxyx(self):
        return self.stdscr.getmaxyx()

    def __getattr__(self, attr):
        """ forwards most attribute/function calls from self.pad, the
        parent drawing surface
        """
        if hasattr(self.pad, attr):
            return getattr(self.pad, attr)
        else:
            raise AttributeError(attr)


def extract_contents(stdscr):
    '''
    Function extract_contents returns the contents of a curses
    window, without (color) attributes.
    '''
    contents = []
    height, width = stdscr.getmaxyx()
    for line in range(height):
        contents.append(stdscr.instr(line, 0))
    contents = [row.decode('utf-8').rstrip() for row in contents]
    return '\n'.join(contents)

def grid_to_glyphs(grid):
    glyphs = []
    height = len(grid)
    for y, row in enumerate(grid):
        width = len(row)
        for x, chars in enumerate(row):
            cell = {'contents': chars, 'x': x, 'y': y}
            cell_glyphs = display.assemble_glyphs(cell, width, height)
            glyphs += cell_glyphs
    return glyphs


class TerminalDrawer(object):

    def draw_state(self, stdscr, grid):
        """
        draw the state of a board onto a curses window.  We assume board is
        simply a double-nested list, rows first. Each row contains a list of
        string to be drawn sequentially, in each column of the grid.
        """
        stdscr.erase()
        xoffset = 0
        self.startx, self.starty = 1, 1
        if self.header:
            self.draw_header_msg(stdscr)
        height = len(grid)
        for y, row in enumerate(grid):
            width = len(row)
            for x, chars in enumerate(row):
                cell = {'contents': chars, 'x': x, 'y': y}
                glyphs = display.assemble_glyphs(cell, width, height)
                for g in glyphs:
                    yy = g.y + self.starty
                    xx = g.x + self.startx + xoffset
                    stdscr.addstr(yy, xx, g.strng, g.attr)
        if self.footer:
            self.draw_footer_msg(stdscr)

    def draw_footer_msg(self, stdscr):
        msg = self.footer
        height, width = stdscr.getmaxyx()
        y = height - 2
        fmt = "{{:^{}}}".format(width)
        msg = fmt.format(msg)
        stdscr.addstr(y, 0, msg)



class TerminalGrid(TerminalDrawer):
    """ the main user-interfacing class. Initialize this to create a
    terminal-based grid on which to play classic Board Games. When you
    wish to draw the grid on the terminal, call draw_grid() with a 2D
    nested list representing the characters you wish to display in the
    grid. The borders of the grid will be automatically calculated.
    Additionally, the function get_input() can be called to receive the
    user's next keypress. This is a blocking call (to your code) and
    won't return until the user has pressed a key
    """
    __locked = []  # used to prevent a 2nd instance spawning
    keyboard = None  # .get() or .push()

    def __init__(self):
        if self.__locked:
            raise IOError('there can only be one terminal instance')
        self.footer = ""
        self.__locked.append(self)
        self.term_input = queue.Queue()
        self._draw_queue = queue.Queue()
        # start terminal, but immediately return control to user
        self.__start_terminal_in_background()

    @concurrent
    def __start_terminal_in_background(self):
        """ function starts terminal, which runs forever, updating
        itself. But since this function is @concurrent decorated, the
        fxn itself returns immediately (while it remains running in the
        background), thus giving control back to the user who
        initialized TermGrid
        """
        self._stdscr = None
        self._run = threading.Event()
        self._run.set()
        curses.wrapper(self.__init_terminal) # blocking until terminal exits
        # below here should run cleanup commands after terminal exits
        self.__locked.clear()  # remove lock preventing multiple terminals
        self._run.clear()  # signal threads to exit

    def __init_terminal(self, stdscr):
        """ Gets called by the curses wrapper. Sets up the initial
        input & state-change queues and then continuously updates the
        terminal screen as new updates are pushed to it
        """
        stdscr.clear()
        if not curses.has_colors():
            curses.start_color()
        curses_colors.colors_init()
        curses.curs_set(0)
        stdscr = FakeStdscr(stdscr)
        # setup term_input to be asyncronously updated with keypresses in
        # the terminal
        inputReader = concurrent(input_reader)
        inputReader(self._run, self.term_input, self._draw_queue, stdscr.getch)
        self.__update_terminal_in_background(self._run, self._draw_queue, stdscr)

    def __update_terminal_in_background(self, run_event, draw_queue, stdscr):
        """ continuously updates the terminal screen as new updates are
        pushed to it. It does not return until run_event is cleared and
        one last update is pushed to draw_queue.
        """
        # read from draw_queue and draw to terminal. Remember, this is run
        # asyncronously
        previous_glyphs = None
        while run_event.is_set():
            event, data = draw_queue.get()
            if event == curses.KEY_RESIZE:
                # terminal was resized. Refresh screen using old data
                self.__draw_glyphs(stdscr, previous_glyphs)
            elif event == 'footer':
                # set footer, but do not overwrite main grid state
                self.footer = data
                self.__draw_glyphs(stdscr, previous_glyphs)
            elif event == 'QUIT':
                print('curses quitting')
                self._run.clear()
                break
            elif event == 'draw glyphs':
                previous_glyphs = data
                self.__draw_glyphs(stdscr, data)
            elif event == 'draw grid':
                previous_glyphs = grid_to_glyphs(data)
                self.__draw_glyphs(stdscr, previous_glyphs)
            else:
                print('unknown command ', event)
            stdscr.refresh()

    def get_input(self):
        """ This gets a character input from the terminal. This function
        will wait indefinitely until a character is pressed, and then
        it'll return the character. 's', 'j', and curses.KEY_ENTER are
        examples
        """
        return self.term_input.get()

    def draw_grid(self, grid_state):
        self._draw_queue.put(('draw grid', grid_state))

    def __draw_glyphs(self, stdscr, glyphs, offset=(1,1)):
        '''draw_glyphs will draw all provided glyphs to stdscr. If offset (a y,
        x number pair) is provided, all glyph coordinates are added to offset
        before being written to stdscr. Offset defaults to (1, 1).'''
        if not glyphs:
            return
        stdscr.erase()
        for g in glyphs:
            offy, offx = offset
            yy = g.y + offy
            xx = g.x + offx
            stdscr.addstr(yy, xx, g.strng, g.attr)
        if self.footer:
            self.draw_footer_msg(stdscr)

    def exit(self):
        self._run.clear()
        # tell the terminal to quit
        self._draw_queue.put(('QUIT', None))

    def set_footer(self, msg):
        self._draw_queue.put(('footer',msg))



if __name__ == '__main__':
    terminal = TerminalGrid()
    terminal.draw_grid([['asdf','fdds'],['(1,0)', '(1,1)']])
    terminal.set_footer('you typed:' + chr(terminal.get_input()))
    # time.sleep(0.5)
    terminal.draw_grid(['abc', '123', 'u&m'])
    time.sleep(2)
    terminal.exit()
    time.sleep(1)

