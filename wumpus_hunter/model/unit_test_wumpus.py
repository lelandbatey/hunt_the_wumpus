import wumpus as w

#pylint: disable=W0312


def test_board_init():
	b = w.Board()
	for x in range(0, b.size):
		for y in range(0, b.size):
			cell = b.grid[x][y]
			assert cell.location[0] == x
			assert cell.location[1] == y




test_board_init()


