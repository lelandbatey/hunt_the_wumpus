
import curses

class SwearJar:
    def __init__(self, stdscr, height, width, screenpos):
        '''
        A very nice container for drawing things to Curses.
        In essence, it acts like a curses.pad, but you can move it's on-screen
        position around with a single variable. Additionally, unlike normal
        pads, you can move a SwearJar off screen and it will behave exactly
        like you think it should.
        '''
        self.stdscr = stdscr
        self.height = height
        self.width = width
        self.screenpos = screenpos
        self.pad = curses.newpad(height, width)

    def refresh(self):
        height, width = self.pad.getmaxyx()
        top = (0, 0)
        screenpos = self.screenpos
        bounding = (screenpos[0]+height-1, screenpos[1]+width-1)
        sy, sx = screenpos
        by, bx = bounding

        # The largest usable y, x coordinates of the screen (bottom left)
        maxy, maxx = self.stdscr.getmaxyx()
        maxy, maxx = maxy-1, maxx-1

        # Ensure that if the pad wants to go off screen but can't, that it is
        # erased instead. Done because we can't actually move a pad off screen,
        # it still needs to be on the screen somehow. As a compromise, we
        # delete the contents of pads that want to be off screen.
        if sy > maxy or sx > maxx:
            self.erase()
        if by < 0 or bx < 0:
            self.erase()

        # When the top right corner of the pad goes off screen, we need to
        # change the starting position of the bounding box so that it doesn't
        # draw the parts of the pad which want to be off screen.
        ty, tx = top
        if sy < 0:
            ty = min(abs(sy), height-1)
        if sx < 0:
            tx = min(abs(sx), width-1)

        # Sanity check to ensure we never pass coordinates that are actually
        # outside of the screen space. Bounding-box coordinates are shrunk in
        # the appropriate dimension(s) to ensure we never try to draw with
        # coordinates off screen.
        sy, sx = min(sy, maxy), min(sx, maxx)
        by, bx = max(by, 0), max(bx, 0)
        self.pad.refresh(ty, tx, sy, sx, by, bx)

    def __getattr__(self, attr):
        """Forwards most attribute/function calls on to self.pad, the
        parent drawing surface.
        """
        if hasattr(self.pad, attr):
            return getattr(self.pad, attr)
        else:
            raise AttributeError(attr)

