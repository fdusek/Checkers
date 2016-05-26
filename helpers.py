from movegen import Movegen
from board import Board
from enums import Piece_type, Faction_type
from piece import Piece
import functools
import json


def get_moves(b, fix_start=False):
	moves = []
	max_seen = 0
	only_promoted_jump = False

	if b.white_plays:
		coords = b.get_white()
	else:
		coords = b.get_black()

	for coord in coords:
		mg = Movegen(b, coord)
		is_promoted = b.get_piece(coord).promoted()

		if (only_promoted_jump == False) or is_promoted:
			for m in mg.get_moves():
				if fix_start:
					m.start_coord_fix = coord
				if (m.attacked_count > max_seen) or (
						is_promoted and (only_promoted_jump == False) and (m.attacked_count > 0)):
					max_seen = m.attacked_count
					moves = [m]
					if is_promoted:
						only_promoted_jump = True
				else:
					if m.attacked_count == max_seen:
						moves.append(m)
	return moves


# def get_white_moves(b):
#	return get_moves(b, True)

# def get_black_moves(b):
#	return get_moves(b, False)

def boardtojson(b, get_next_moves=True):
	to_return = {}
	for coord in b.iter_coords():
		if b.get_piece(coord) is not None:
			p = b.get_piece(coord)
			ptype = ""
			if p.promoted() == True:
				ptype = "promoted "
			if p.faction() == Faction_type.white:
				ptype += "piece white "
			if p.faction() == Faction_type.black:
				ptype += "piece black "

			if coord[1] not in to_return:
				to_return[coord[1]] = {}
			to_return[coord[1]][coord[0]] = {"type": ptype, "next_moves": []}
	if get_next_moves:
		for move in get_moves(b, True):
			#move.get_board().bprint()
			y, x = move.start_coord_fix
			to_return[x][y]["next_moves"].append({"end_coord": (move.end_coord[1], move.end_coord[0]),
												  "next_state": boardtojson(move.get_board(), False)})

	return to_return


def jsontoboard(j, white_plays):
	if isinstance(j, str):
		j = json.loads(j)
	b = Board(white_plays)
	b.state = [[None] * 8 for x in range(4)]
	for keya, vala in j.items():
		for keyb, valb in vala.items():
			if "WHITE" in valb["type"].upper():
				if "PROMOTED" in valb["type"].upper():
					b._set_piece((int(keyb), int(keya)), Piece_type.white_promoted)
				else:
					b._set_piece((int(keyb), int(keya)), Piece_type.white)
			if "BLACK" in valb["type"].upper():
				if "PROMOTED" in valb["type"].upper():
					b._set_piece((int(keyb), int(keya)), Piece_type.black_promoted)
				else:
					b._set_piece((int(keyb), int(keya)), Piece_type.black)
	return b


def strtoboard(strdata):
	strdata = strdata.replace(" ", "").split("\n")
	mat = []
	white_plays = None
	for line in strdata:
		line_translated = []
		if "Whiteplays" in line:
			white_plays = True
			continue
		if "Blackplays" in line:
			white_plays = False
			continue

		for c in line:
			if (c == "w"):
				line_translated.append((Piece(Piece_type.white)))
			if (c == "W"):
				line_translated.append((Piece(Piece_type.white_promoted)))
			if (c == "b"):
				line_translated.append((Piece(Piece_type.black)))
			if (c == "B"):
				line_translated.append((Piece(Piece_type.black_promoted)))
			if (c == "_"):
				line_translated.append(None)
		if len(line_translated) > 0:
			mat.append(line_translated)

	if white_plays is None:
		raise ValueError("Board data didn't contain information about who plays")

	return Board(white_plays=white_plays, board_state=[list(reversed(line)) for line in matrix_rotate(mat, 90)])


def matrix_rotate(matrix, degree):
	if abs(degree) not in [0, 90, 180, 270, 360]:
		raise ValueError('Cannot rotate board by {0}, valid rotation values are 0, 90, 180, 270, 360'.format(degree))
	if degree == 0:
		return matrix
	elif degree > 0:
		return matrix_rotate(list(zip(*matrix[::-1])), degree - 90)
	else:
		return matrix_rotate(list(zip(*matrix))[::-1], degree + 90)
