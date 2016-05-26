from flask import Flask, jsonify, request
from helpers import *
from board import Board
from search import alphabetapicker
import time
import json

app = Flask(__name__)


@app.route('/')
def index_route():
	return app.send_static_file('index.html')


@app.route('/new')
def hello_world():
	b = Board(True)
	return jsonify(boardtojson(b))


@app.route('/solve', methods=['POST'])
def solve():
	result = request.get_json()
	jsontoboard(result, False).bprint()
	all_white_moves = get_moves(jsontoboard(result, False))
	new_b = alphabetapicker(all_white_moves)
	new_b.bprint()
	return json.dumps(boardtojson(new_b))


if __name__ == '__main__':
	app.run(debug=True)
