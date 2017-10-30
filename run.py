
import tkinter as tk
import argparse

from wumpus_hunter import game_logic
from wumpus_hunter.model import wumpus
from wumpus_hunter.ui.wump_tk import GameWindow
from wumpus_hunter.ui.wump_term import entrypoint

def main():
   parser = argparse.ArgumentParser(description='Play hunt the wumpus.')
   parser.add_argument('--gui', type=bool, default=False, help='Whether to launch the game in a GUI window instead of the terminal (default is "false").')
   args = parser.parse_args()

   if args.gui:
      board = game_logic.NewGame(wumpus.Difficulties.Easy)
      root = tk.Tk()
      gwin = GameWindow(root, board, height=500, width=800)
      root.mainloop()
      return

   entrypoint()

if __name__ == '__main__':
   main()
