from checkers import *
import time

b = Board(board_empty = True)
try:
	b._set_piece((1, 1), Piece_type.white_promoted)
	print("FAIL: setting invalid coord")
except ValueError: 
	print("PASS: setting invalid coord")

try:
	p = b.get_piece((1, 1))
	print("FAIL: getting invalid coord")
except ValueError: 
	print("PASS: getting invalid coord")

b = Board(board_empty = True)
try:
	b._set_piece((1, 2), Piece_type.white_promoted)
	p = b.get_piece((1, 2))
	print("PASS: getting or setting valid coord")
except ValueError:
	print("FAIL: getting or setting VALID coord")


if p.promoted():
	print("PASS: piece set to promoted")
else:
	print("FAIL: piece not set to promoted")

if len(p.vectors()) == 4:
	print("PASS: count of vectors valid")
else:
	print("FAIL: count of vectors not valid")

if p.faction() == Faction_type.white:
	print("PASS: faction valid")
else:
	print("FAIL: faction not valid")


b = Board(board_empty = True)
try:
	b._set_piece((2, 3), Piece_type.black)
	p = b.get_piece((2, 3))
	print("PASS: getting or setting valid coord")
except ValueError:
	print("FAIL: getting or setting VALID coord")

if not p.promoted():
	print("PASS: piece not set to promoted")
else:
	print("FAIL: piece set to promoted")

if len(p.vectors()) == 2:
	print("PASS: count of vectors valid")
else:
	print("FAIL: count of vectors not valid")

if p.faction() == Faction_type.black:
	print("PASS: faction valid")
else:
	print("FAIL: faction not valid")

flipflop = None
broken = False
for x in range(0, b.size-1):
	for y in range(0, b.size-1):
		if flipflop == None:
			flipflop = b.is_valid_coord((x, y))
		else:
			if flipflop == b.is_valid_coord((x, y)):
				broken = True
				break
			flipflop = not flipflop
if broken:			
	print("FAIL: Valid coord is not returning chequered pattern")
else:
	print("PASS: Valid coord is returning chequered pattern")

b = Board(board_empty = True)
b._set_piece((1, 2), Piece_type.black_promoted)
p1 = b.get_piece((1, 2))
b._set_piece((2, 3), Piece_type.black)
p2 = b.get_piece((2, 3))

if not b.is_same_faction((1, 2), (2, 3)):
	print("FAIL: Same faction check A")
else:
	print("PASS: Same faction check A")

b = Board(board_empty = True)
b._set_piece((1, 2), Piece_type.black)
p1 = b.get_piece((1, 2))
b._set_piece((2, 3), Piece_type.white_promoted)
p2 = b.get_piece((2, 3))

if b.is_same_faction((1, 2), (2, 3)):
	print("FAIL: Same faction check B")
else:
	print("PASS: Same faction check B")

b = Board()
branchfactor = []
try:
	while True:
		all_moves = get_white_moves(b)
		branchfactor.append(len(all_moves))
		new_move = random.choice(all_moves)
		before_black = len(list(b.iter_black()))
		before_white = len(list(b.iter_white()))
		b = new_move.get_board()
		after_black = len(list(b.iter_black()))
		after_white = len(list(b.iter_white()))
		if before_white != after_white:
			print("FAIL: There was white piece removed during white move")
			break

		if new_move.attacked_count != (before_black - after_black):
			print("FAIL: Diff between iter black before and iter black after move is different than attacked pieces")
			print("Diff = " + str(before_black - after_black))
			print("attacked_count = " + str(new_move.attacked_count))
			break

		#b.bprint()
		#print("Attacked count = "+ str(new_move.attacked_count))
		#print("="*20)
		#print()
		#print("="*20)

		all_moves = get_black_moves(b) 
		branchfactor.append(len(all_moves))
		new_move = random.choice(all_moves)

		before_black = len(list(b.iter_black()))
		before_white = len(list(b.iter_white()))
		b = new_move.get_board()
		after_black = len(list(b.iter_black()))
		after_white = len(list(b.iter_white()))
		if before_black != after_black:
			print("FAIL: There was black piece removed during black move")
			break

		if new_move.attacked_count != (before_white - after_white):
			print("FAIL: Diff between iter white before and after move is different than attacked pieces")
			print("Diff = " + str(before_white - after_white))
			print("attacked_count = " + str(new_move.attacked_count))
			break
		#b.bprint()
		#print("Attacked count = "+ str(new_move.attacked_count))
		#print("="*20)
		#print()

		#input("Press enter to cont...")
except IndexError as e:
	print("PASS: Attack moves counts")
	

