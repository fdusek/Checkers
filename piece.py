from enums import *


class Piece(object):
	def __init__(self, piece_type):
		if isinstance(piece_type, Piece_type):
			self.ptype = piece_type
		else:
			raise ValueError("Piece type has to be instance of 'class Piece_type (Enum)' it is " + str(piece_type))

	def promoted(self):
		piece_type = self.ptype
		if (piece_type == Piece_type.black_promoted) or (piece_type == Piece_type.white_promoted):
			return True
		else:
			return False

	def vectors(self):
		if self.promoted():
			return [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # this piece can move in all diagonal directions
		if self.ptype == Piece_type.black:
			return [(1, 1), (-1, 1)]  # this piece can move up diagonally
		if self.ptype == Piece_type.white:
			return [(1, -1), (-1, -1)]  # this piece can move down diagonally
		raise ValueError("This piece does not have move vectors defined for its type. Piece type = " + str(self.ptype))

	def __eq__(self, other):
		return (other is not None) and (self.ptype == other.ptype)

	def faction(self):
		piece_type = self.ptype
		# print(self.ptype)

		if (piece_type == Piece_type.black) or (piece_type == Piece_type.black_promoted):
			return Faction_type.black

		if (piece_type == Piece_type.white) or (piece_type == Piece_type.white_promoted):
			return Faction_type.white
		raise ValueError(
			"This piece does not have a Faction_type. Did you forget to remove highlighted piece? Piece type is " + str(
				self.ptype))
