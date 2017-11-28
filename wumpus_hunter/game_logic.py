import random

from .model.wumpus import Player, Wumpus, Gold, Pit, Board, Difficulties

GAME_SETTINGS = {
	Difficulties.Easy: {
		"size": 8,
		"wumpus_count": 1,
		"gold_count_range": (10, 15),
		"pit_count_range": (10, 15)
	},
	Difficulties.Medium: {
		"size": 9,
		"wumpus_count": 1,
		"gold_count_range": (10, 15),
		"pit_count_range": (15, 20)
	},
	Difficulties.Hard: {
		"size": 10,
		"wumpus_count": 2,
		"gold_count_range": (15, 20),
		"pit_count_range": (15, 20)
	},
}

class Keys:
	NORTH = 'N'
	SOUTH = 'S'
	WEST = 'W'
	EAST = 'E'

def NewGame(difficulty):
	'''Returns a new Board object constructed with the state for the provided
	difficulty.'''
	settings = GAME_SETTINGS[difficulty]

	board_size = settings['size']

	gold_val = 100
	gold_range = settings['gold_count_range']
	gold_count = random.sample(range(*gold_range), 1)[0]

	pit_val = -50
	pit_range = settings['pit_count_range']
	pit_count = random.sample(range(*pit_range), 1)[0]

	wumpii_val = -10000
	wumpii_count = settings['wumpus_count']

	# Create all the unique random tile positions to place Entities.
	all_entity_count = 1 + gold_count + pit_count + wumpii_count
	yxs = set(sample_random_points(all_entity_count, 0, board_size))
	while len(yxs) < all_entity_count:
		yxs.add(sample_random_points(1, 0, board_size)[0])
	coordinates = list(yxs)
	random.shuffle(coordinates)

	golds = [Gold(coordinates.pop(), gold_val) for _ in range(gold_count)]
	pits = [Pit(coordinates.pop(), pit_val) for _ in range(pit_count)]
	wumpii = [Wumpus(coordinates.pop(), wumpii_val) for _ in range(wumpii_count)]

	# Ensure that the player can't be a wumpus location.
	player_location = coordinates.pop()
	player = Player(player_location)

	board = Board(player, wumpii, golds, pits, difficulty, settings['size'])

	# Now that we have a board, we can add the correct callbacks to our wumpii
	for wumpus in wumpii:
		wumpus.arrow_enter_callback = create_wumpus_kill(board)
		wumpus.player_enter_callback = create_player_enter_wump(board)

	# Additionally, we can add callbacks for when the player enters
	for g in golds:
		g.player_enter_callback = create_default_player_enter(board)
	for p in pits:
		p.player_enter_callback = create_default_player_enter(board)

	return board

def create_wumpus_kill(board):
	def wumpus_kill(wumpus):
		'''Game logic for killing a wumpus.'''
		if wumpus.living:
			wumpus.living = False
			board.points += 200
			board.sound = "SCREAM!"
	return wumpus_kill

def create_player_enter_wump(board):
	def player_enter_wump(wumpus):
		if wumpus.living:
			board.add_points(wumpus.point_value)
		if not (wumpus.living or wumpus.visited):
			# If the player finds a dead wumpus for the first time, they get a
			# points bonus of 50 points
			board.add_points(50)
		wumpus.visited = True

def create_default_player_enter(board):
	def default_player_enter(entity):
		try:
			if not entity.visited:
				board.add_points(entity.point_value)
				entity.visited = True
		except Exception:
			pass
	return default_player_enter

def sample_random_points(point_count, minimum, maximum):
	"""Returns a list of random coordinate pairs.
	Each coordinate is within the given minimum and maximum ( [min,max) )."""
	randrange = list(range(minimum, maximum))
	return [(random.sample(randrange, 1)[0], random.sample(randrange, 1)[0]) for _ in range(point_count)]
