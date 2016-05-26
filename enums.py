from enum import Enum


class Piece_type(Enum):
	white = 1
	black = 2
	white_promoted = 3
	black_promoted = 4
	empty_highlight = -1


class Faction_type(Enum):
	no_faction = 0
	white = 1
	black = 2
