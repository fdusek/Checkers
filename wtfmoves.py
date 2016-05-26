def wtf():
	dat = """w   w   w   w
	w   w   w   w
	  _   w   _   w
	_   _   _   _
	  _   w   b   _
	b   _   b   _
	  b   b   b   b
	b   b   b   b"""
	b = strtoboard(dat)
	b.bprint()
	mvs = get_black_moves(b)
	#print(mvs)

	#b.bprint()

def wtf2():
	dat = """w   w   w   w
w   _   w   w
  b   b   w   _
_   _   _   w
  w   b   _   b
_   b   _   _
  _   b   b   b
b   b   b   b"""
	b = strtoboard(dat)
	b.bprint()

	moves = []
	m = Movegen(b, (0, 1))
	moves.extend(m.get_moves())
	b = random.choice(moves).get_board()
	b.bprint()

def wtf3():
	dat = """w   w   w   w
_   _   w   w
  _   _   _   _
_   _   _   w
  _   _   _   b
_   _   _   b
  _   _   _   _
_   _   _   _"""
	b = strtoboard(dat)
	b.bprint()

	moves = []
	m = Movegen(b, (6, 5))
	moves.extend(m.get_moves())
	b = random.choice(moves).get_board()
	b.bprint()

def wtf4():
	dat = """_   _   B   w   
_   _   _   w   
  w   _   _   w   
_   _   _   _   
  w   _   _   _   
b   b   _   _   
  b   w   _   _   
b   _   _   _   """
	b = strtoboard(dat)
	b.bprint()

	moves = []
	m = Movegen(b, (6, 2))
	moves.extend(m.get_moves())
	b = random.choice(moves).get_board()
	b.bprint()


def checkhash():
	dat = """0 1 2 3 4 5 6 7 
 0   _   w   w   w   
 1 _   w   w   w   
 2   _   _   _   w   
 3 _   _   _   _   
 4   _   _   b   b   
 5 w   _   b   _   
 6   W   _   _   b   
 7 _   _   _   _ """
	b = strtoboard(dat)
	print(b.__hash__())	
	dat = """0 1 2 3 4 5 6 7 
 0   _   w   w   w   
 1 _   w   w   w   
 2   _   _   _   w   
 3 _   _   _   _   
 4   _   _   b   b   
 5 _   _   _   _   
 6   W   _   _   b   
 7 _   _   _   _ """
	b = strtoboard(dat)
	print(b.__hash__())	
	dat = """0 1 2 3 4 5 6 7 
 0   _   w   w   w   
 1 _   w   w   w   
 2   _   _   _   w   
 3 _   _   _   _   
 4   _   _   b   b   
 5 w   _   b   _   
 6   W   _   _   b   
 7 _   _   _   _ """
	b = strtoboard(dat)
	print(b.__hash__() ^ 
		b.zobrist_vals[((0, 5), Piece_type.white)] ^ 
		b.zobrist_vals[((4, 5), Piece_type.black)])	


	def wtf4():
	dat = """_   _   B   w   
_   _   _   w   
  w   _   _   w   
_   _   _   _   
  w   _   _   _   
b   b   _   _   
  b   w   _   _   
b   _   _   _   """
	b = strtoboard(dat)
	b.bprint()

	moves = []
	m = Movegen(b, (2, 5))
	moves.extend(m.get_moves())
	b = random.choice(moves).get_board()
	b.bprint()

def wtfnega():
	dat = """ 0   _   w   w   w   
	1 _   w   w   w   
	2   w   w   w   w   
	3 w   _   _   _   
	4   b   b   b   _   
	5 b   b   _   _   
	6   _   b   b   b   
	7 b   b   b   _   """
	b = strtoboard(dat)
	b.bprint()
	mvs = get_white_moves(b)
	b.highlight([negamaxpicker(mvs, True)])
	b.bprint()


def wtfnega2():
	dat = """White plays
   0 1 2 3 4 5 6 7 
 0   _   w   w   w   
 1 _   w   w   w   
 2   _   _   _   w   
 3 _   _   _   _   
 4   _   _   b   b   
 5 w   _   b   _   
 6   W   _   _   b   
 7 _   _   _   _ """
	b = strtoboard(dat)
	b.bprint()
	mvs = get_white_moves(b)
	b.highlight(mvs)
	b.bprint()
	b.dehighlight()
	b.highlight([negamaxpicker(mvs, True)])
	b.bprint() 
	b.dehighlight()


