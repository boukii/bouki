import os
import random
import time
import unittest
from abc import ABCMeta, abstractmethod

width = 7
height = 6
iJugadores = [1 , 2]
jugador = 0

class LetsPlay(object):
	width = 7
	height = 6
	board = [[0 for y in range(height)]for x in range (width)]
	currentPlayer = None
	finished = False
	winner = None
	players = [None, None]
	gameFinished = False
	currentNumberPlayer = iJugadores

	def __init__(self):
		if jugador != 1:
			self.players[0] = _HumanP(self.currentNumberPlayer[0]) 
			self.players[1] = _IA(self.currentNumberPlayer[1])
		else:
			self.players[0] = _IA(self.currentNumberPlayer[0]) 
			self.players[1] = _HumanP(self.currentNumberPlayer[1])

	def start(self):
		while not self.gameFinished:
			self._next_move()

	def start_new(self):
		self.currentPlayer = self.players[jugador]
		self.start()

	def _switch_player(self):
		if self.currentPlayer == self.players[0]:
			self.currentPlayer = self.players[1]
		else:
			self.currentPlayer = self.players[0]

	def _next_move(self):
		column = self.currentPlayer.get_move(self.board)
		for i in range(self.height -1, -1, -1):
			if self.board[i][column] == 0:
				self.board[i][column] = self.currentPlayer._number
				self._switch_player()
				return
		print("This column is full. Please choose an other column")
		return

###################################################################
	def _check_status(self):
		""" Check and update the status of the game
		"""
		if self._is_full():
			self.finished = True
		elif self._is_connect_four():
			self.finished = True
			self.winner = self.currentPlayer

	def _is_full(self):
		"""
		Check if the grid is full
        :return: Boolean
        """
		 # the number of round can't be superior to the number of case of the grid
		return self._round > self.width * self.height

	def _is_connect_four(self):
		"""
		Check if there is a connect four in the grid
		:return: Boolean
		"""
		# for each box of the grid
		for i in xrange(self.height - 1, -1, -1):
			for j in xrange(self.width):
				if self.board[i][j] != ' ':
					# check for vertical connect four
					if self._find_vertical_four(i, j):
						return True

					# check for horizontal connect four
					if self._find_horizontal_four(i, j):
						return True

					# check for diagonal connect four
					if self._find_diagonal_four(i, j):
						return True

		return False

	def _find_vertical_four(self, row, column):
		"""
        Check for vertical connect four starting at index [row][column] of the grid
        :param row: row of the grid
        :param column: column of the grid
        :return: Boolean
        """
		consecutiveCount = 0

		if row + 3 < self.height:
			for i in xrange(4):
				if self.board[row][column] == self.board[row + i][column]:
					consecutiveCount += 1
				else:
					break

			# define the winner
			if consecutiveCount == 4:
				if self.players[0]._number == self.board[row][column]:
					self.winner = self.players[0]
				else:
					self.winner = self.players[1]
				return True

		return False

	def _find_horizontal_four(self, row, column):
		"""
        Check for horizontal connect four starting at index [row][column] of the grid
        :param row: row of the grid
        :param column: column of the grid
        :return: Boolean
        """
		consecutiveCount = 0

		if column + 3 < self.width:
			for i in xrange(4):
				if self.board[row][column] == self.board[row][column + i]:
					consecutiveCount += 1
				else:
					break

			# define the winner
			if consecutiveCount == 4:
				if self.players[0]._number == self.board[row][column]:
					self.winner = self.players[0]
				else:
					self.winner = self.players[1]
				return True

		return False

	def _find_diagonal_four(self, row, column):
		"""
        Check for diagonal connect four starting at index [row][column] of the grid
        :param row: row of the grid
        :param column: column of the grid
        :return: Boolean
        """
		consecutiveCount = 0
		# check positive slope
		if row + 3 < self.height and column + 3 < self.width:
			for i in xrange(4):
				if self.board[row][column] == self.board[row + i][column + i]:
					consecutiveCount += 1
				else:
					break

			# define the winner
			if consecutiveCount == 4:
				if self.players[0]._number == self.board[row][column]:
					self.winner = self.players[0]
				else:
					self.winner = self.players[1]
				return True

		consecutiveCount = 0
		# check negative slope
		if row - 3 >= 0 and column + 3 < self.width:
			for i in xrange(4):
				if self.board[row][column] == self.board[row - i][column + i]:
					consecutiveCount += 1
				else:
					break

			# define the winner
			if consecutiveCount == 4:
				if self.players[0]._number == self.board[row][column]:
					self.winner = self.players[0]
				else:
					self.winner = self.players[1]
				return True

		return False

	def _print_state(self):
		""" Print state of the game (round, grid, winner)
		"""
		# cross-platform clear screen
		os.system(['clear', 'cls'][os.name == 'nt'])
		# print the round
		print("             Round: " + str(self._round))
		print("")
		# print the grid
		for i in xrange(self.height):
			print("\t"),
			for j in xrange(self.width):
				print("| " + str(self.board[i][j])),
			print("|")
		print("\t"),
		# print the bottom of the grid with columns index
		for k in xrange(self.width):
			print("  _"),
		print("")
		print("\t"),
		for k in xrange(self.width):
			print("  %d" % (k + 1)),
		print("")
		# print final message when the game is finished
		if self.finished:
			print("Game Over!")
			if self.winner != None:
				print(str(self.winner.type) + " is the winner!")
			else:
				print("Game is a draw")


class _Player(object):
	global board, width, height
	metalclass = ABCMeta
	type = None
	_number = None

	def __init__(self, number):
		self._number = number

	@abstractmethod
	def get_move(self, board):
		pass

class _HumanP(_Player):
	global board, width, height

	def __init__(self, number):
		super(_HumanP, self).__init__(number)
		self.type = "Human"

	def get_move(self, board):
		column = None
		while column == None:
			try:
				column = int(input("Your turn: ")) -1
			except ValueError:
				column = None
			if 0 <= column <= 6:
				return column
			else:
				column = None
				print("Please, enter a number between 1 and 6")

class _IA(_Player):

	global board, width, height
	_Dificulty = 5

	def __init__(self, number):
		super(_IA, self).__init__(number)
		self.type = "IA"

	def get_move(self, board):
		return self._get_best_move(board)

	def _get_best_move(self, board):
		if self._number == iJugadores[0]:
			human_number = iJugadores[1]
		else:
			human_number = iJugadores[0]
		legal_moves = {}
		for column in range(width):
			if self._is_legal_move(column, board):
				tmp_board = self._simulate_move(board, column, self._number)
				legal_moves[column] = -self._find(self._Dificulty - 1, tmp_board, human_number)
		best_alpha = -99999999
		best_move = None
		moves = legal_moves.items()
		for move, alpha in moves:
			if alpha >= best_alpha:
				best_alpha = alpha
				best_move = move
		return best_move

	def _find(self, depth, board, player_number):
		legal_moves = []
		for i in range(height):
			if self._is_legal_move(i, board):
				tmp_board = self._simulate_move(board, i, player_number)
				legal_moves.append(tmp_board)
			if depth == 0 or len(legal_moves) == 0 or self._game_is_over(board):
				return self._eval_game(depth, board, player_number)
		if player_number == iJugadores[0]:
			opp_player_number = iJugadores[1]
		else:
			opp_player_number = iJugadores[0]
		alpha = -99999999
		for child in legal_moves:
			if child == None:
				print("child == None (search)")
			alpha = max(alpha, -self._find(depth - 1, child, opp_player_number))
		return alpha

	def _is_legal_move(self, column, board):
		for i in range(height -1, -1, -1):
			if board[i][column] == 0:
				return True
		return False

	def _game_is_over(self, board):
		if self._find_streak(board, iJugadores[0], 4) > 0:
			return True
		elif self._find_streak(board, iJugadores[1], 4) > 0:
			return True
		else:
			return False

	def _simulate_move(self, board, column, number):
		tmp_board = [x[:] for x in board]
		for i in range(height -1, -1, -1):
			if tmp_board[i][column] == 0:
				tmp_board[i][column] = number
				return tmp_board

	def _eval_game(self, depth, board, currentPlayer):
		if currentPlayer == players[0]:
			opp_player_number = players[1]
		else:
			opp_player_number = players[0]
			ia_fours = self._find_streak(board, currentPlayer, 4)
			ia_threes = self._find_streak(board, currentPlayer, 3)
			ia_twos = self._find_streak(board, currentPlayer, 2)
			human_fours = self._find_streak(board, currentPlayer, 4)
			human_threes = self._find_streak(board, currentPlayer, 3)
			human_twos = self._find_streak(board, currentPlayer, 2)
			if human_fours > 0:   
				return -100000 - depth
			else:
				return (ia_fours * 100000 + ia_threes * 100 + ia_twos * 10) - (human_threes * 100 + human_twos * 10) + depth

	def _find_streak(self, board, currentPlayer, streak):
		count = 0
		for i in range(height):
			for j in range(width):
				print (board[i][j])
				print (currentPlayer)
				if board[i][j] == currentPlayer:
					count += self.test_check_vertical_right(i, j, board, streak)
					count += self.test_check_vertical_left(i, j, board, streak)
					count += self.test_check_horizontal_up(i, j, board, streak)
					count += self.test_check_horizontal_down(i, j, board, streak)
					count += self.test_check_diagonal_left_down(i, j, board, streak)
					count += self.test_check_diagonal_left_up(i, j, board, streak)
					count += self.test_check_diagonal_right_down(i, j, board, streak)
					count += self.test_check_diagonal_right_up(i, j, board, streak)
		return count

	def _find_vertical_streak(self, row, column, board, streak):
		consecutiveCount = 0
		if row + streak - 1 < height:
			for i in range(streak):
			    if grid[row][column] == board[row + i][column]:
			    	consecutiveCount += 1
			    else:
			    	break

		if consecutiveCount == streak:
			return 1
		else:
			return 0

	def _find_horizontal_streak(self, row, column, board, streak):
		consecutiveCount = 0
		if column + streak - 1 < width:
			for i in range(streak):
				if board[row][column] == board[row][column + i]:
					consecutiveCount += 1
				else:
					break

		if consecutiveCount == streak:
			return 1
		else:
			return 0

	def _find_diagonal_streak(self, row, column, board, streak):
		total = 0
		consecutiveCount = 0
		if row + streak - 1 < height and column + streak - 1 < width:
			for i in range(streak):
				if board[row][column] == board[row + i][column + i]:
					consecutiveCount += 1
				else:
					break

		if consecutiveCount == streak:
			total += 1

		consecutiveCount = 0
		if row - streak + 1 >= 0 and column + streak - 1 < width:
			for i in range(streak):
				if board[row][column] == board[row - i][column + i]:
					consecutiveCount += 1
				else:
					break

		if consecutiveCount == streak:
			total += 1
		return total

class TestCasses(unittest.TestCase):

	def setUp(self):
		self.letsPlayT = LetsPlay()

	def test_check_vertical_right(self):
		boardT = [
			[iJugadores[0],0,0,0,0,0,0],
			[iJugadores[0],iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_vertical_left(self):
		boardT = [
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],iJugadores[0]],
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_horizontal_up(self):
		boardT = [
			[iJugadores[0],iJugadores[0],iJugadores[0],0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_horizontal_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[iJugadores[0], iJugadores[0], iJugadores[0],0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_diagonal_left_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[iJugadores[0],0,iJugadores[0],0,0,0,0],
			[0, iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,0,0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_diagonal_left_up(self):
		boardT = [
			[iJugadores[0],0,0,0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,iJugadores[0],0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_diagonal_right_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],0],
			[0,0,0,0,iJugadores[0],0,iJugadores[0]]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_check_diagonal_right_up(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,iJugadores[0],0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],0],
			[0,0,0,0,0,0,iJugadores[0]]
		]
		self.letsPlayT.board = boardT
		self.assertEqual(self.letsPlayT._is_connect_four(), True)

	def test_is_full(self):
		self.assertEqual(self.letsPlayT._is_full(), True)

class TestIACasses(unittest.TestCase):

	def setUp(self):
		self.letsPlayT = LetsPlay()

	def test_check_vertical_right(self):
		boardT = [
			[iJugadores[0],0,0,0,0,0,0],
			[iJugadores[0],iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_vertical_left(self):
		boardT = [
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],iJugadores[0]],
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]		
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)


	def test_check_horizontal_up(self):
		boardT = [
			[iJugadores[0],iJugadores[0],iJugadores[0],0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_horizontal_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[iJugadores[0], iJugadores[0], iJugadores[0],0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_diagonal_left_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[iJugadores[0],0,iJugadores[0],0,0,0,0],
			[0, iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,0,0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_diagonal_left_up(self):
		boardT = [
			[iJugadores[0],0,0,0,0,0,0],
			[0,iJugadores[0],0,0,0,0,0],
			[iJugadores[0],0,iJugadores[0],0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_diagonal_right_down(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],0],
			[0,0,0,0,iJugadores[0],0,iJugadores[0]]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_check_diagonal_right_up(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,iJugadores[0],0,iJugadores[0]],
			[0,0,0,0,0,iJugadores[0],0],
			[0,0,0,0,0,0,iJugadores[0]]
		]
		self.assertEqual(self.letsPlayT.players[1]._find_streak(boardT,iJugadores[1], 4),1)

	def test_ia_intelligence_1(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0, iJugadores[1], iJugadores[0],0,0,0],
			[0, iJugadores[1], iJugadores[0], iJugadores[0],0,0,0],
			[0, iJugadores[1], iJugadores[0], iJugadores[0],0,0,0],
			[0, iJugadores[1], iJugadores[0], iJugadores[1], iJugadores[0], 0, iJugadores[1]]
			[0, iJugadores[1], iJugadores[0], iJugadores[1], iJugadores[0], 0, iJugadores[1]]
		]
		self.assertEqual(self.letsPlayT.players[1].get_move(boardT), 1)
		

	def test_ia_intelligence_2(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0]
		]
		self.assertEqual(self.letsPlayT.players[1].get_move(boardT), 5)

	def test_ia_intelligence_3(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0, iJugadores[1],0,0,0,0],
			[0, iJugadores[0], iJugadores[0], iJugadores[0],0,0,0],
			[0, iJugadores[1], iJugadores[0], iJugadores[0],0,0, iJugadores[1]],
			[0, iJugadores[1], iJugadores[0], iJugadores[1], iJugadores[0],0, iJugadores[1]]
		]
		self.assertEqual(self.letsPlayT.players[1].get_move(boardT), 1)

	def test_ia_intelligence_4(self):
		boardT = [
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0],
			[iJugadores[0],0,0,0,0,0,0],
		]
		self.assertEqual(self.letsPlayT.players[1].get_move(boardT), 6)

def main():
	global board, width, height
	letplay = LetsPlay()
	jugador = input("Quien va a Empezar? (1) o (2)")
	bAux = False
	iAux = 0
	while bAux == False:
		letplay.start_new()
		iAux = input("Volver a Jugar? (1) Si (2) No")
		if iAux == 1:
			bAux = False
		else:
			bAux = True

if __name__ == '__main__':
	main()
	unittest.main()
