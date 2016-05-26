from cache import Cache
from helpers import *
from collections import Counter


def score_board(b):
	allfields = [b.get_piece(coord) for coord in b.iter_coords()]
	allpiecetypes = [piece.ptype for piece in allfields if piece is not None]
	c = Counter(allpiecetypes)
	print(c)
	score = (c[Piece_type.white_promoted] * 2 + c[Piece_type.white]) - c[Piece_type.black_promoted] * 2 - c[
		Piece_type.black]
	return score


def minmax(node, depth):
	child_nodes = [m.get_board() for m in get_moves(node)]
	if (depth == 0) or (len(child_nodes) == 0):
		return score_board(node)

	if node.white_plays:
		bestvalue = float("-inf")
		for child in child_nodes:
			score = minmax(child, depth - 1)
			bestvalue = max(bestvalue, score)
		return bestvalue
	else:
		bestvalue = float("inf")
		for child in child_nodes:
			score = minmax(child, depth - 1)
			bestvalue = min(bestvalue, score)
		return bestvalue


def alphabeta(node, depth, alpha=float("-inf"), beta=float("inf"), cache=None):
	if cache is None:
		cache = Cache(1000)
	cached_result = cache.get(node)

	if (cached_result is not None):
		if (cached_result[0] >= depth):
			return cached_result[1]

	child_nodes = [m.get_board() for m in get_moves(node)]
	if (depth == 0) or (len(child_nodes) == 0):
		return score_board(node)

	if node.white_plays:
		bestvalue = alpha
		for child in child_nodes:
			ab_score = alphabeta(child, depth - 1, bestvalue, beta, cache=cache)  # , bla = ab_score2)
			bestvalue = max(bestvalue, ab_score)

			if beta <= bestvalue:
				break
		cache.add(node, bestvalue, depth)
		return bestvalue
	else:
		bestvalue = beta
		for child in child_nodes:
			ab_score = alphabeta(child, depth - 1, alpha, bestvalue, cache=cache)  # , bla = ab_score2)

			bestvalue = min(bestvalue, ab_score)
			if bestvalue <= alpha:
				break

		cache.add(node, bestvalue, depth)
		return bestvalue


def alphabeta_nocache(node, depth, alpha=float("-inf"), beta=float("inf")):
	child_nodes = [m.get_board() for m in get_moves(node)]
	if (depth == 0) or (len(child_nodes) == 0):
		return score_board(node)

	if node.white_plays:
		bestvalue = alpha
		for child in child_nodes:
			ab_score = alphabeta(child, depth - 1, bestvalue, beta)
			bestvalue = max(bestvalue, ab_score)

			if beta <= bestvalue:
				break
		return bestvalue
	else:
		bestvalue = beta
		for child in child_nodes:
			ab_score = alphabeta(child, depth - 1, alpha, bestvalue)
			bestvalue = min(bestvalue, ab_score)
			if bestvalue <= alpha:
				break
		return bestvalue


def alphabetapicker_nocache(next_level_moves, depth=6):
	next_level_boards = [move.get_board() for move in next_level_moves]

	scores = [(b, alphabeta(b, depth)) for b in next_level_boards]
	best = max(scores, key=lambda x: x[1])

	return best[0]


def alphabetapicker(next_level_moves, depth=6, white_should_win = False):
	next_level_boards = [move.get_board() for move in next_level_moves]
	scores = [(b, alphabeta(b, depth)) for b in next_level_boards]
	print(scores)
	if white_should_win:
		best = max(scores, key=lambda x: x[1])
	else:
		best = min(scores, key=lambda x: x[1])

	return best[0]
