from enums import *
from board import Board
from piece import Piece


def clone_board_state(board):
	return [list(x) for x in board.state]


class Move(object):
	def __init__(self, board, start_coord, end_coord, attacked = None, attacked_count = 0):		
		self.white_plays = board.white_plays
		self.state = board.state
		self.start_coord = start_coord
		self.end_coord = end_coord
		self.attacked = attacked
		self.attacked_count = attacked_count

	def get_board(self):
		return Board(white_plays = self.white_plays, board_state = self.state, apply_move = self)