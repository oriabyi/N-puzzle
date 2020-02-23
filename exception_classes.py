import sys


class NpuzzleError(Exception):
	pass


class WrongMatrixSize(NpuzzleError):
	def __init__(self):
		print('Wrong matrix size!', file=sys.stderr)
