from checkers import *
import random, time
from collections import Counter
from cache import Cache
from search import alphabetapicker
from helpers import *


def playgame(watchgame=False, scores=False, move_picker=random.choice, v=False):
	global ww
	global bw
	b = Board(white_plays=True)
	play = True
	branching_factor = []
	random.seed(time.time())
	mc = 0
	while play:
		mc += 1
		all_white_moves = get_moves(b)
		# print(score_moves(all_white_moves))
		if len(all_white_moves) > 0:
			branching_factor.append(len(all_white_moves))
			new_board = move_picker(all_white_moves)
			b = new_board
		else:
			play = False
			bw += 1
			print("Black player won. gg.\r\n")
			break
		if watchgame:
			print("White player played, the game has score {0}".format(score_board(b)))
			# print("Hash of this board is "+str(b.__hash__()))
			b.bprint()
			input("Any key to continue...")

		all_black_moves = get_moves(b)
		# print(score_moves(all_black_moves))
		if len(all_black_moves) > 0:
			branching_factor.append(len(all_black_moves))
			new_board = random.choice(all_black_moves)
			b = new_board.get_board()
		else:
			play = False
			ww += 1
			print("White player won. gg.\r\n")
			break
		if watchgame:
			print("Black player played, the game has score {0}".format(score_board(b)))
			# print("Hash of this board is "+str(b.__hash__()))
			b.bprint()
			input("Any key to continue...")
		if mc > 7: break
	return branching_factor, score_board(b)


ww = 0
bw = 0


def benchmark(move_count, v=False, watchgame=False, move_picker=random.choice):
	time_start = time.time()
	scores = []
	for i in range(0, move_count):
		branching_factor, score = playgame(v=v, watchgame=watchgame, move_picker=move_picker)
		cnt = len(branching_factor)
		sm = sum(branching_factor)
		scores.append(score)
		print(
			"On average each state in this game had {0} successor states.\r\nGame had {1} moves.\r\nAnd score {2}.".format(
				int(sm / cnt * 100) / 100, cnt, score))

	score_cnt = len(branching_factor)
	score_sm = sum(branching_factor)

	print("Average score = {0}".format(score_sm / score_cnt))
	print("White wins = {0}".format(ww))
	print("Black wins = {0}".format(bw))
	print("Average nodes expanded for one search = ", total_ab / search_count)

	time_end = time.time()
	inmsecs = (time_end - time_start) * 1000
	print("Time elapsed is {0} ms".format(int((inmsecs * 100)) / 100))


def da_game():
	dat = ("Black plays  \n"
		   "   0 1 2 3 4 5 6 7 \n"
		   " 0   _   _   _   _   \n"
		   " 1 _   _   w   _  \n"
		   " 2   _   _   _   _   \n"
		   " 3 _   _   w   _   \n"
		   " 4   b   _   _   w   \n"
		   " 5 b   _   _   _   \n"
		   " 6   b   w   _   w   \n"
		   " 7 _   W   w   w   \n"
		   " ")
	b = strtoboard(dat)
	# all_white_moves = get_moves(b)
	# time_start = time.time()

	# new_b = alphabetapicker(all_white_moves)
	# new_b.bprint()
	# new_b.bprint()

	jsontoboard(boardtojson(b), True).bprint()


# time_end = time.time()
# inmsecs = (time_end - time_start)*1000
# print("Time elapsed is {0} ms".format(int((inmsecs*100))/100))

# new_b.bprint()


da_game()
