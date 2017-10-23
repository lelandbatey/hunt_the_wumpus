
import tkinter as tk
import base64
import os.path
import os

from .. import game_logic
from ..model import wumpus

SPRITEMAP = {
    wumpus.Wumpus: 'wumpus.gif',
    wumpus.Gold: 'gold.gif',
    wumpus.Pit: 'pit.gif',
    wumpus.Player: 'medChar.gif'
}

class SpriteCollection(object):
    def __init__(self, path=None):
        if path is None:
            path = os.path.abspath("./")
        # Assume that we're running in the code repo root
        self.imgdir = os.path.join(path, "wumpus_hunter/ui/images")
        self.images = dict()
        for p in os.listdir(self.imgdir):
            if not p.endswith('.gif'):
                continue
            imgpath = os.path.join(self.imgdir, p)
            disp_obj = tk.PhotoImage(file=imgpath)
            self.images[p] = disp_obj
            self.images[imgpath] = disp_obj
            # with open(imgpath, 'rb') as image:
                # data = base64.b64encode(image.read())

def canv_coords_cell(board, cell, canvas):
    '''Returns a tuple with three locations:
        0: the canvas coordinate of the top left corner of the GameCell
        1: the canvas coordinate of the bottom right corner of the GameCell
        2: the canvas coordinate of the center point of the GameCell
    Each location is itself a y,x coordinate pair, as a tuple.'''
    canv_width = (int(canvas['width'])-1)
    cell_width = canv_width // board.size
    centering_offset = (canv_width % board.size) // 2
    celly, cellx = cell.location
    # Right now assumes a totally square canvas, may need to change in future
    topy, topx = (celly*cell_width)+centering_offset, (cellx*cell_width)+centering_offset
    middley, middlex = topy+(cell_width//2), topx+(cell_width//2)
    lowy, lowx = topy+cell_width, topx+cell_width
    return ((topy, topx), (lowy, lowx), (middley, middlex))


class GameWindow(tk.Frame):
    def __init__(self, parent, board, *args, **kwargs):
        self.board = board
        super().__init__(parent, *args, **kwargs)
        # Setting "highlightthickness" is important for correct display, see this SO:
        #     https://stackoverflow.com/a/15892182
        self.canvas = tk.Canvas(self, height=400, width=400, background='white', highlightthickness=0)
        self.sprites = SpriteCollection()
        self.items = []

        for direction, _ in wumpus.DIRECTIONS.items():
            cmd = generate_move_func(direction, self.board, self)
            btn = tk.Button(parent, text=direction, command=cmd)
            btn.pack(fill=tk.X)
        self.pack()
        self.redraw()
        self.canvas.pack()

    def redraw(self):
        # re-draws all sprites onto the board
        while self.items:
            self.canvas.delete(self.items.pop())
        for row in self.board.grid:
            for cell in row:
                pos = canv_coords_cell(self.board, cell, self.canvas)
                upr_left, lwr_right, middle = pos
                # print(cell.location, pos)
                # self.canvas.create_text(middle text=str(cell.location))
                # self.canvas.create_rectangle((upr_left, lwr_right))
                for ent in cell.contents:
                    entity_img = SPRITEMAP[ent.__class__]
                    sprite = self.sprites.images[entity_img]
                    item = self.canvas.create_image(middle, image=sprite)
                    # print("Drawing", entity_img, "with id", item, "at location", cell.location)
                    self.items.append(item)
        # Draw our player on top
        ent = self.board.player
        center_point = canv_coords_cell(self.board, ent, self.canvas)[2]
        entity_img = SPRITEMAP[ent.__class__]
        sprite = self.sprites.images[entity_img]
        item = self.canvas.create_image(center_point, image=sprite)
        # print("Drawing player", self.board.player, entity_img, "with id", item, "at location", ent.location)
        self.canvas.tag_raise(item)
        self.items.append(item)


def generate_move_func(direction, board, game_win):
    def move_func():
        board.traverse(board.player, direction)
        game_win.redraw()
    return move_func


if __name__ == '__main__':
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    root = tk.Tk()
    gwin = GameWindow(root, board, height=500, width=800)

    root.mainloop()
