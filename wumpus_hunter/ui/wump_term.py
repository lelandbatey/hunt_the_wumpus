
import time

from .. import game_logic
from ..model import wumpus

from .term import sweargrid, display

def summarize_contents(cell):
    rv = ""
    for ent in cell.contents:
        if isinstance(ent, wumpus.Wumpus):
            rv += "W"
        if isinstance(ent, wumpus.Gold):
            rv += "G"
        if isinstance(ent, wumpus.Pit):
            rv += "P"
        if isinstance(ent, wumpus.Player):
            rv += "X"
    return rv

def fmt_sense(sensations):
    keys = sorted(list(sensations.keys()))
    fmt = ""
    for k in keys:
        if sensations[k]:
            fmt += k[0]
        else:
            fmt += '-'
    return fmt

def print_game(board):

    for row in board.grid:
        print()
        for cell in row:
            senses = board.derive_sensations(cell.location)
            # print(" {} ".format(summarize_contents(cell)), end=' ')
            # print(fmt_sense(senses), end=' ')
            print(cell.location, end=' ')
        print()
    print("Score:", board.points)

def demonstrate_move(board):
    for _ in range(10):
        print_game(board)
        y, x = board.player.location
        board.move(board.player, (y, x+1))
        time.sleep(0.2)

def update_and_refresh(board, tg):
    grid_state = []
    for row in board.grid:
        row_strings = []
        for cell in row:
            senses = board.derive_sensations(cell.location)
            row_strings.append(fmt_sense(senses))
        grid_state.append(row_strings)
    tg.draw_grid(grid_state)
    time.sleep(2)
    tg.get_input()
    tg.exit()
    time.sleep(0.1)

def entrypoint():
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    terminal = sweargrid.TerminalGrid()
    update_and_refresh(board, terminal)

if __name__ == '__main__':
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    # print_game(board)
    demonstrate_move(board)

