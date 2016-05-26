import sqlite3
import os


class Cache(object):
	def __init__(self, commit_every):
		self.commit_every = commit_every
		self.buffer = {}
		self.conn = sqlite3.connect('checkers_cache.db')
		self.c = self.conn.cursor()
		self.c.execute("CREATE TABLE IF NOT EXISTS cache (hash INT PRIMARY KEY, depth INT, score REAL)")
		self.conn.commit()

	def add(self, board, score, depth):
		self.buffer[board] = (depth, score)
		if len(self.buffer) >= self.commit_every:
			self.commit()

	def commit(self):
		vals = [(item.__hash__(), key[0], key[1]) for item, key in self.buffer.items()]
		self.c.executemany("INSERT OR REPLACE INTO cache VALUES (?, ?, ?)", vals)
		self.buffer = {}
		self.conn.commit()

	def get(self, b):
		if b in self.buffer:
			return self.buffer[b]
		else:
			self.c.execute("SELECT * FROM cache WHERE hash = " + str(b.__hash__()))
			result = self.c.fetchone()
			return result if result is None else (result[1], result[2])  # returns None if nothing found_

	def __del__(self):
		self.commit()
