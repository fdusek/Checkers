from enums import *
from move import Move


class Movegen(object):
	def __init__(self, board, start_coord):
		self.board = board
		self.start_coord = start_coord

	def get_moves_in_direction(self, board, start_coord, vector, step_limit=1, only_attack=False):
		moves = []
		# print()
		# print("----------------")
		# print("starting search from ", end="")
		# print(start_coord)
		drop_if_next_empty = False
		piece_attacked = None
		if board.is_empty(start_coord):
			raise ValueError(
				"Selected field is empty, can't move with piece X: {0} Y: {1}".format(start_coord[0], start_coord[1]))

		steps_done = 0
		for current_coord in board.piece_walk(start_coord, vector):
			# print("Steps done {0}, step limit {1}".format(steps_done, step_limit))
			if steps_done < step_limit:
				# print("Current_coord = ", end = "")
				# print(current_coord)
				# board.bprint()
				if board.is_empty(current_coord):
					# we can jump on this field. lets save this coord
					if only_attack:
						##print("only attack")
						if piece_attacked is not None:
							new_move = Move(board=board, start_coord=start_coord, end_coord=current_coord, attacked=piece_attacked, attacked_count=1)
							moves.append(new_move)
							steps_done += 1
						else:
							steps_done += 1
					else:
						if drop_if_next_empty:
							moves = []
							drop_if_next_empty = False
						# print("Droping all previous moves, because we have to jump.")
						att_count = 1 if piece_attacked is not None else 0
						new_move = Move(board=board, start_coord=start_coord, end_coord=current_coord, attacked=piece_attacked, attacked_count=att_count)
						moves.append(new_move)
						# print("Appending current coord!")
						steps_done += 1
					# print("Steps done = {0}, steps max = {1}".format(steps_done, step_limit))
				else:
					if board.is_same_faction(start_coord, current_coord):
						# we can't jump over or on our own pieces, search would be pointless from now on. break.
						# print("breaking because same faction")
						break
					else:
						if (piece_attacked is None) and (not drop_if_next_empty):
							# print("attacking = ", end = "")
							# print(current_coord)
							piece_attacked = current_coord
							drop_if_next_empty = True
						# if next field will be empty, jumping there will be an attacking move! coooool!
						# and if that is true, all the moves we found until now will be invalid,
						# because previous moves were nonattacking and if we can, we HAVE to attack
						else:
							# print("breaking because piece was already attacked, do next search")
							# print(piece_attacked)
							break
						# looks like we could either:
						# a) we successfully finished jumping over piece before and this looks like an opportunity to jump over next one,
						#    but this function searches only for first possible attack move.
						#    run it again with new to get new attack possibilities.
						# b) we attacked something before, but next place is not empty, so we can't jump over it
						# and that is why we break here!
			else:
				break
		return moves

	def get_moves_no_multijumps(self, board, start_coord, only_attack=False, step_limit=None):
		possible = []
		promoted = board.get_piece(start_coord).promoted()
		for vector in board.get_piece(start_coord).vectors():
			# board.bprint()
			moves = []
			if promoted:
				step_limit = 1000
			else:
				if step_limit is None:
					step_limit = 1

			moves = self.get_moves_in_direction(board, start_coord, vector, step_limit=step_limit, only_attack=only_attack)
			if len(moves) > 0:
				if not only_attack:
					for move in moves:
						if move.attacked is not None:
							only_attack = True
							possible = [prev_move for prev_move in possible if
										prev_move.attacked is not None]  # can be optimized by building attacked list in loop before!!
							break
				possible.extend(moves)
		return possible

	def get_moves(self, only_attack=False):
		new_stack = self.get_moves_no_multijumps(self.board, self.start_coord, only_attack=only_attack)
		stack = []

		while len(new_stack) > 0:
			stack = new_stack
			new_stack = []
			for move in stack:
				if move.attacked is not None:
					att = move.attacked_count
					for new_move in self.get_moves_no_multijumps(move.get_board(), move.end_coord, only_attack=True, step_limit=1):
						new_move.attacked_count = att + 1
						new_stack.append(new_move)

		for mv in stack:
			mv.white_plays = not mv.white_plays

		return stack
