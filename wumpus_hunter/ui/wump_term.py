
from .. import game_logic
from ..model import wumpus

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


def print_game(board):
    def fmt_sense(sensations):
        keys = sorted(list(sensations.keys()))
        fmt = ""
        for k in keys:
            if sensations[k]:
                fmt += k[0]
            else:
                fmt += '-'
        return fmt

    for row in board.grid:
        print()
        for cell in row:
            # senses = board.derive_sensations(cell.location)
            print(" {} ".format(summarize_contents(cell)), end=' ')
            # print(cell, end=' ')
            # print(cell.location, end=' ')
        print()



if __name__ == '__main__':
    board = game_logic.NewGame(wumpus.Difficulties.Easy)
    print_game(board)

