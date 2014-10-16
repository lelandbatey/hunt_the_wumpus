from __future__ import print_function
import random 
import time


def sample_random_points(point_count, minimum, maximum):
    """Returns a list of random X,Y pairs.
    Each coordinate is within the given minimum and maximum."""
    samples = [\
        random.sample(range(minimum, maximum), point_count),
        random.sample(range(minimum, maximum), point_count)]
    return [[samples[0][i], samples[1][i]] for i in range(len(samples[0]))]


class Room(object):
    """Represents a single room and all it's attributes."""
    def __init__(self, board, row, column, wumpus=False):
        super(Room, self).__init__()
        self.row = row
        self.column = column
        self.board = board
        self.wumpus = wumpus
        self.treasure = False
        self.pit = False

        # Tracks whether user has visited this room
        self.visited = False
        # Will be the string with the sense readout 
        self.sense_info = ''
    def has_tresure(self):
        """Checks if the room contains treasure.""" 
        return self.treasure
    
    def has_pit(self):
        """Checks if this room contains a pit."""
        return self.pit

    def has_wumpus(self):
        """Checks if a Wumpus is in this room."""
        return self.wumpus

    def is_clear(self):
        """Checks if this room contains nothing at all."""
        return not (self.wumpus or self.pit or self.treasure)


class Character(object):
    """The player character."""
    def __init__(self, board):
        super(Character, self).__init__()
        self.board = board
        self.row, self.column = None, None
    
    def place_character(self):
        """Places the character in an empty room on the board."""
        while not (self.row or self.column):
            for row, col in sample_random_points(1, 0, self.board.size):
                room = self.board.get_room(row, col)
                if room.is_clear():
                    self.row, self.column = room.row, room.column
        return self.row, self.column

    def move_character(self, direction):
        """Attempts to move the character in the given direction.

        Direction must be a string, and can be either 'l', 'r', 'u', or 'd',
        each one standing for different direction (left, right, up, down). 
        """
        dir_map = {
            'u': [-1, 0],
            'd': [1, 0],
            'l': [0, -1],
            'r': [0, 1]
        }
        row_delta, col_delta = dir_map[direction]

        # Checks that the move would still put us on the board.
        if self.row+row_delta in range(self.board.size) and\
        self.column+col_delta in range(self.board.size):
            self.row += row_delta
            self.column += col_delta







        

class GameBoard(object):
    """Contains all the different rooms on the board."""
    def __init__(self, size):
        super(GameBoard, self).__init__()
        self.size = size
        self.board_structure = []
        self.points = 0
        self.character = Character(self)

        # Builds our empty board_structure
        for rows in range(size):
            row = []
            for columns in range(size):
                row.append(Room(self, rows, columns))
            self.board_structure.append(row)

        def get_room(self, row, col):
            """Attempts to return the requested room."""
            if not (row in range(self.size) and col not in range(self.size)):
                raise IndexError("The requested room coordinates are invalid.")
            return self.board_structure[row, col]






if __name__ == '__main__':
    print(sample_random_points(5, 0, 10))


        
    



