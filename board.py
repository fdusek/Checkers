from enums import *
from piece import Piece
import random

def get_zobrist_vals(b):
	global zobrist_vals
	if zobrist_vals is None:
		result = {}
		random.seed(235926)
		for coord in b.iter_coords():
			for en in Piece_type:
				if en.value >= 0:
					result[(coord, en)] = random.randint(- 2 ** 63 + 1, 2 ** 63 - 1)
		result["white_plays"] = random.randint(- 2 ** 63 + 1, 2 ** 63 - 1)
		zobrist_vals = result
	return zobrist_vals


zobrist_vals = None


class Board(object):
	def __init__(self, white_plays, board_state=None, board_empty=False, apply_move=None, zobrist_help=None):
		self.size = 8
		self.hash = None
		self.white_plays = white_plays
		if board_state is not None:
			self.state = [list(row) for row in board_state]
			if apply_move is not None:
				print("apply")
				# print(apply_move.start_coord)
				p = self.get_piece(apply_move.start_coord)
				ptype = p.ptype

				ydir = p.vectors()[0][1]
				ypos = apply_move.end_coord[1]
				ymax = self.size - 1

				promote = True if ((ydir < 0) and (ypos == 0)) or ((ydir > 0) and (ypos == ymax)) else False
				
				if promote:
					if ptype == Piece_type.white:
						ptype = Piece_type.white_promoted
						print(self)
					if ptype == Piece_type.black:
						ptype = Piece_type.black_promoted
						print(self)

				self._set_piece(apply_move.end_coord, ptype)
				self._set_piece(apply_move.start_coord, None)

				if apply_move.attacked is not None:
					self._set_piece(apply_move.attacked, None)
				if promote:
					print(self)

		else:
			if self.size % 2 == 0:
				self.state = [[None for y in range(self.size)] for x in range(self.size // 2)]
				if not board_empty:
					for x in range(0, self.size):
						for y in range(0, 3):
							if self.is_valid_coord((x, y)):
								self._set_piece((x, y), Piece_type.black)
					for x in range(0, self.size):
						for y in range(5, self.size):
							if self.is_valid_coord((x, y)):
								self._set_piece((x, y), Piece_type.white)
				# self._set_piece((3, 4), Piece_type.black)
				# self._set_piece((1, 2), Piece_type.black)
				# self._set_piece((0, 1), None)
				# self._set_piece((5, 6), Piece_type.black)
				# self._set_piece((3, 4), Piece_type.black)
				# self._set_piece((4, 1), None)
				# self._set_piece((0, 1), Piece_type.white)
				# self._set_piece((1, 0), None)
			else:
				raise ValueError('Cannot create board with size {0}. Board size must be even number.'.format(self.size))
		self.zobrist_vals = get_zobrist_vals(self)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		result = "white plays" if self.white_plays else "Black plays"
		dct = {Piece_type.white: "w", Piece_type.white_promoted: "W", Piece_type.black: "b", Piece_type.black_promoted: "B", None: "_", Piece_type.empty_highlight: "#"}
		result += "\r\n"
		rot90 = self.matrix_rotate(self.state, -90)
		s = "   "
		for i in range(0, len(rot90)):
			s = s + str(i) + " "
		result = result + s + "\r\n"
		for x in range(0, len(rot90)):
			result = result + " " + str(x) + " "
			if x % 2 == 0:
				result += "  "
			x_len = len(rot90)
			for y in range(0, len(rot90[x])):
				# print(y, end = "")
				try:
					result += "{0}   ".format(dct[rot90[x_len - 1 - x][y].ptype])
				except AttributeError:
					result += "_   "
			result += "\r\n"
		return result

	def get_white(self):
		return self.get_faction(True)

	def get_black(self):
		return self.get_faction(False)

	def get_faction(self, white):
		promoted = []
		normal = []

		for p in self.iter_faction(white):
			if self.get_piece(p).promoted():
				promoted.append(p)
			else:
				normal.append(p)

		promoted.extend(normal)
		return promoted

	def iter_white(self):
		return self.iter_faction(True)

	def iter_black(self):
		return self.iter_faction(False)

	def iter_faction(self, white):
		if white:
			faction_check = Faction_type.white
		else:
			faction_check = Faction_type.black

		for coord in self.iter_coords():
			p = self.get_piece(coord)
			if p is not None:
				if p.faction() == faction_check:
					yield coord

	def get_piece(self, coord):
		x, y = coord
		if self.is_valid_coord(coord):
			return self.state[x // 2][y]
		else:
			raise ValueError(
				'Coord (X: {0} Y: {1}) is pointing out of the chessboard or on field where piece should never be.'.format(
					coord[0], coord[1]))

	def is_valid_coord(self, coord):
		x, y = coord

		x_odd = (x % 2) != 0
		y_odd = (y % 2) != 0

		if (x >= 0) and (x < self.size) and (y >= 0) and (y < self.size):
			if y_odd:
				if x_odd:
					return False
			else:
				if not x_odd:
					return False
			return True
		else:
			return False

	def is_same_faction(self, coord_a, coord_b):
		faction_a = self.get_piece(coord_a).faction()
		faction_b = self.get_piece(coord_b).faction()

		if faction_a == faction_b:
			return True
		else:
			return False

	def is_empty(self, coord):
		if self.get_piece(coord) is None:
			return True
		else:
			return False

	def piece_step(self, coord, vector):
		dx, dy = vector
		x, y = coord
		return x + dx, y + dy

	def matrix_rotate(self, matrix, degree):
		if abs(degree) not in [0, 90, 180, 270, 360]:
			raise ValueError(
				'Cannot rotate board by {0}, valid rotation values are 0, 90, 180, 270, 360'.format(degree))
		if degree == 0:
			return matrix
		elif degree > 0:
			return self.matrix_rotate(list(zip(*matrix[::-1])), degree - 90)
		else:
			return self.matrix_rotate(list(zip(*matrix))[::-1], degree + 90)

	def highlight(self, moves):
		print("WARNING: Don't forget to run dehighlight before playing.")
		end_places = [move.end_coord for move in moves]

		for coord in end_places:
			self._set_piece(coord, Piece_type.empty_highlight)

	def dehighlight(self):
		for coord in self.iter_coords():
			p = self.get_piece(coord)
			if p is not None:
				if p.ptype == Piece_type.empty_highlight:
					self._set_piece(coord, None)

	def iter_coords(self):
		for x in range(0, self.size, 2):
			for y in range(0, self.size):
				if (y % 2) == 0:
					yield (x + 1, y)
				else:
					yield (x, y)

	def _set_piece(self, coord, piece):
		x, y = coord
		# print("before", x, "  ", y)
		# self.bprint()
		if self.is_valid_coord(coord):
			if piece != None:
				self.state[x // 2][y] = Piece(piece)
			else:
				self.state[x // 2][y] = None
			# print("after")
			# self.bprint()

		else:
			raise ValueError(
				'Coord (X: {0} Y: {1}) is pointing out of the chessboard or on field where piece should never be.'.format(
					coord[0], coord[1]))

	def piece_walk(self, coord, vector):  # walk in one direction without checking any rules
		piece_position = self.piece_step(coord, vector)
		while self.is_valid_coord(piece_position):
			yield piece_position
			piece_position = self.piece_step(piece_position, vector)

	def __eq__(self, other):
		return isinstance(other, Board) and (self.white_plays == other.white_plays) and (self.state == other.state)

	def __hash__(self):
		if self.hash is None:
			for coord in self.iter_coords():
				p = self.get_piece(coord)
				if p is not None:
					if self.hash == None:
						self.hash = self.zobrist_vals[(coord, p.ptype)]
					else:
						self.hash = self.hash ^ self.zobrist_vals[(coord, p.ptype)]
			self.hash = self.hash ^ self.zobrist_vals["white_plays"]
		return self.hash

	def bprint(self):
		print(self.__str__())
