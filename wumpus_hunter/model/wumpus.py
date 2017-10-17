from __future__ import print_function
import random


class Difficulties:
    Easy = "easy_diff"
    Medium = "medium_diff"
    Hard = "hard_diff"


DIRECTION = {'u': [-1, 0], 'd': [1, 0], 'l': [0, -1], 'r': [0, 1]}


class CellEntity(object):
    """CellEntity is for any object which has an x,y location on the board."""

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.location)


class GameItem(CellEntity):
    """Represents an item on the board which we the player interact with such
    as an item or adversary."""

    def __init__(self,
                 location,
                 point_value,
                 player_enter_callback=None,
                 arrow_enter_callback=None):
        super().__init__(location)
        self.point_value = point_value
        self.arrow_enter_callback = arrow_enter_callback
        self.player_enter_callback = player_enter_callback
        self.visited = False


class Player(CellEntity):
    """Player object."""

    def __init__(self, location):
        super().__init__(location)


class Wumpus(GameItem):
    """Wumpus object. Wumpus *does* require both a player_enter_callback and an
    arrow_enter_callback for correct operation, though they may be set after
    construction if need be."""

    def __init__(self,
                 location,
                 point_value=-1000,
                 player_enter_callback=None,
                 arrow_enter_callback=None):
        super().__init__(location, point_value, player_enter_callback,
                         arrow_enter_callback)
        self.living = True

    def kill(self):
        """ kills the wumpus. Return # of points awarded for killing the wumpus, then set it's point value (for being found, physically) to a positive value
        """
        if self.living == True:
            self.living = False
            self.arrow_enter_callback(self)


class Pit(GameItem):
    """Pit object"""

    def __init__(self, location, point_value=-200, **kwargs):
        super().__init__(location, point_value, **kwargs)


class Gold(GameItem):
    """Gold object"""

    def __init__(self, location, point_value, **kwargs):
        super().__init__(location, point_value, **kwargs)


class GridCell(CellEntity):
    """Object represents the cells of a game grid."""

    def __init__(self, location):
        super().__init__(location)
        self.contents = []


class Board(object):
    """Object for the board. The variables"""

    def __init__(self, player, wumpii, golds, pits, difficulty="", size=6):
        self.difficulty = difficulty
        self.size = size
        self.sound = None
        self.points = 0
        self.grid = [[GridCell([h, w]) for w in range(0, self.size)]
                     for h in range(0, self.size)]

        self.player = player
        self.wumpii = wumpii
        self.golds = golds
        self.pits = pits

        # Place the entities into the gridcells on the board. We expect each
        # entity we've been provided to have it's valid x,y coordinates set
        # already, so we just place them where they're to go. Validation of
        # acceptable locations for each game item is done in the game logic.
        entities = [
            x for lst in [self.wumpii, self.golds, self.pits] for x in lst
        ]
        entities += [self.player]
        for ent in entities:
            y, x = ent.location
            self.grid[y][x].contents.append(ent)

    def add_points(self, p):
        self.points += p

    def grid_iter(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def move(self, entity, location):
        """ move entity to location. It is assumed that the entity.location
            attribute is not changed beforehand
        """
        y, x = entity.location
        self.grid[y][x].contents.remove(entity)
        entity.location = location
        y, x = location
        self.grid[y][x].contents.append(entity)

    def get_nearby(self, location):
        deltas = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        nearby = dict()
        y, x = location
        for k in deltas.keys():
            dy, dx = deltas[k]
            ny, nx = [a + b for a, b in zip((y, x), (dy, dx))]
            # board is square, so self.size is a single integer
            # we still need to check that y, x are within its bounds
            if nx in range(self.size) and ny in range(self.size):
                nearby[k] = self.grid[ny][nx]
            else:
                nearby[k] = None
        return nearby

    def derive_sensations(self, location):
        '''Returns a dictionary of the sensations the player experiences in
        their current cell.'''
        y, x = location
        nearby = self.get_nearby(location)
        senses = {'glint': False, 'breeze': False, 'stench': False}
        for _, v in nearby.items():
            if not v: continue
            for ent in v.contents:
                if isinstance(ent, Wumpus):
                    senses['stench'] = True
                if isinstance(ent, Gold):
                    senses['glint'] = True
                if isinstance(ent, Pit):
                    senses['breeze'] = True
        return senses


if __name__ == '__main__':
    print(sample_random_points(5, 0, 10))
