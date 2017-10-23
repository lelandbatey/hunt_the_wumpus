
import tkinter as tk

from wumpus_hunter import game_logic
from wumpus_hunter.model import wumpus
from wumpus_hunter.ui.wump_tk import GameWindow

board = game_logic.NewGame(wumpus.Difficulties.Easy)
root = tk.Tk()
gwin = GameWindow(root, board, height=500, width=800)

root.mainloop()
