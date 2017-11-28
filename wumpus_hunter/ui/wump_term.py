
import time
import curses

from .. import game_logic
from ..model import wumpus

from .term import sweargrid, display
from ..game_logic import Keys


KEYMAP = {
    # arrow keys
    curses.KEY_UP: Keys.NORTH,
    curses.KEY_DOWN: Keys.SOUTH,
    curses.KEY_LEFT: Keys.WEST,
    curses.KEY_RIGHT: Keys.EAST,
    # wasd
    ord('w'): Keys.NORTH,
    ord('s'): Keys.SOUTH,
    ord('a'): Keys.WEST,
    ord('d'): Keys.EAST,
    # vim keybindings
    ord('k'): Keys.NORTH,
    ord('j'): Keys.SOUTH,
    ord('h'): Keys.WEST,
    ord('l'): Keys.EAST,
}


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
    player = board.player
    dirty_cache = []
    for row in board.grid:
        row_strings = []
        for cell in row:
            row_strings.append("   ")
        dirty_cache.append(row_strings)
    refresh_board(board, tg, dirty_cache)
    while True:
        try:
            key = tg.get_input()
        except KeyboardInterrupt:
            break
        direction = KEYMAP.get(key)
        if direction:
            board.traverse(player, direction)
            refresh_board(board, tg, dirty_cache)
    tg.exit()
    time.sleep(0.1)

def refresh_board(board, tg, dirty_cache):
    player = board.player
    y, x = player.location
    for r, row in enumerate(board.grid):
        for c, cell in enumerate(row):
            if cell.location == player.location:
                senses = board.derive_sensations(cell.location)
                dirty_cache[r][c] = fmt_sense(senses)
    tg.draw_grid(dirty_cache)

def entrypoint():
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    terminal = sweargrid.TerminalGrid()
    update_and_refresh(board, terminal)

if __name__ == '__main__':
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    # print_game(board)
    demonstrate_move(board)

