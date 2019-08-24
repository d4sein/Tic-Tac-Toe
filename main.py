from random import randint, choice
from itertools import cycle


class Player():
	'''Instance of the player'''
	def __init__(self, mark, moves):
		self.mark = mark
		self.moves = moves


class Bot():
	'''Instance of the bot'''
	def __init__(self, mark, moves):
		self.mark = mark
		self.moves = moves


class Game:
	'''Instance of the game'''
	def __init__(self, table: list, slots: list, available: list, player: object, bot: object) -> None:
		self.table = table
		self.slots = slots
		self.available = available
		self.player = player
		self.bot = bot

	def show_table(self) -> None:
		'''Shows current table'''
		for row in self.table:
			[print(f'[{pos}]', end='') for pos in row]; print()

	def get_play(self, turn: object) -> int:
		'''Gets a valid play'''
		if not self.available:
			return None

		if turn == self.player:
			while True:
				try:
					move = int(input('Move: '))
				except ValueError:
					print('Invalid move.')
					continue

				if move not in self.available:
					print('You can\'t play here.')
					continue

				break
		else:
			move = choice(self.available)

		self.available.remove(move)

		if move < 4: self.table[0][(move - 1) % 3] = turn.mark
		elif move < 7: self.table[1][(move - 1) % 3] = turn.mark
		else: self.table[2][(move - 1) % 3] = turn.mark

		return move

	def get_resolution(self, turn: list) -> bool:
		'''Checks for winning turn'''
		# the loop generates a sequence to access all the possible winning combinations
		for row, column in zip(range(0, 7, 3), range(0, 3)):
			if all(i in turn for i in self.slots[row:3 + row]) or all(i in turn for i in self.slots[column::3]):
				return True

			if all(i in turn for i in self.slots[::4]) or all(i in turn for i in self.slots[2:8:2]):
				return True

		return False

	def run(self, turn: object) -> bool:
		'''Runs the game'''
		self.show_table()
		move = self.get_play(turn)

		if move == None:
			return True
		else:
			turn.moves.append(move)
		
		return self.get_resolution(turn.moves)


def generate_game(row: list, column: int) -> object:
	'''Generates all substantial info'''
	# creates matrix for table
	table = [row[i:i + column] for i in range(0, len(row), column)]
	# gets all valid moves from table
	slots = [item for row in table for item in row]
	available = slots.copy()
	# randomly sets player and bot marks
	pMark, bMark = ('\033[1;31mX\033[0m', '\033[1;34mO\033[0m') if randint(1, 100) <= 50 else ('\033[1;34mO\033[0m', '\033[1;31mX\033[0m')

	# instantiates the objects
	player = Player(pMark, [])
	bot = Bot(bMark, [])
	game = Game(table, slots, available, player, bot)

	return game


def main():
	# defines matrix dimension
	row, column = (list(range(1, 10)), 3)
	game = generate_game(row, column)

	pattern = (game.player, game.bot) if game.player.mark == 'X' else (game.bot, game.player)
	for turn in cycle(pattern):
		if game.run(turn):
			print(); game.show_table()

			if not game.available:
				print('Draw!')
			else:
				print('Player won!' if turn == game.player else 'Bot won!')
			break

		print()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
