import argparse
import sys

from exception_classes import *


def parse_files(args_list):
	return (parse_file(arg) for arg in args_list)


def parse_file(arg):
	try:
		return [el for el in open(arg)]
	except NameError:
		print('Wrong file %s!' % arg, file=sys.stderr)
		return False
	except PermissionError:
		return False
	except FileNotFoundError:
		return False


def get_matrix_size(matrix_size_line):
	try:
		return int(matrix_size_line)
	except ValueError:
		raise WrongMatrixSize


def check_nums_in_matrix(matrix, matrix_size, from_file=True):
	if from_file:
		return sorted(el for group in matrix for el in group) == list(range(matrix_size**2))
	return sorted(el for el in matrix) == list(range(matrix_size**2))


def remove_comments(data):
	for i in range(len(data)):
		if '#' in data[i]:
			data[i] = data[i][:data[i].index('#')]
	return data


def group_convert_to_int(clear_matrix, from_file=True):
	try:
		if from_file:
			int_grouped_matrix = []

			for x in [char_matrix.split() for char_matrix in clear_matrix]:
				int_grouped_matrix.append([int(el) for el in x])
			return int_grouped_matrix
		else:
			return [int(el) for el in clear_matrix]
	except ValueError:
		return []


def remove_empty_elements(data):
	return [el for el in data if el]


def validate_data(data, from_file=True, matrix_size=0):
	rstripped_data = remove_empty_elements([line.rstrip() for line in data])

	if from_file:
		try:
			matrix_size = get_matrix_size(rstripped_data[0])
		except WrongMatrixSize:
			return False
		rstripped_data = rstripped_data[1:]

	clear_matrix = remove_comments(rstripped_data)
	int_grouped_matrix = group_convert_to_int(clear_matrix, from_file)
	if not check_nums_in_matrix(int_grouped_matrix, matrix_size, from_file):
		print('There are something wrong with data in matrix!', file=sys.stderr)
		return False
	return int_grouped_matrix


def validate_data_files(data):
	return [validate_data(el) for el in data]


def receive_input_data():
	try:
		matrix_size = get_matrix_size(input())
	except WrongMatrixSize:
		return False
	i = 0
	input_data = ''
	while i < matrix_size:
		temp = input()
		input_data += temp + ' '
		i += 1
	formatted_data = validate_data(input_data, False, matrix_size)
	print(formatted_data)


if __name__ == "__main__":
	parse_arguments = argparse.ArgumentParser(description='The goal of this project is to solve the N-puzzle ("taquin" in French) '
											'game using the A*search algorithm or one of its variants.')
	parse_arguments.add_argument('-f', '--file', type=str, help='specify path to file with map', action='append')
	parse_arguments.add_argument('-s', '--string', help='specify map in cmd', default=None, action='count')
	parse_arguments.add_argument('-t', '--test')

	# TODO: try parse file, string or throw err
	args = parse_arguments.parse_args()
	if args.file and args.string:
		print('Ты чё, волчонок? Ты дохуя умный? Слышишь, ты чё нах?')
	elif args.file:
		data = parse_files(args.file)
		print(validate_data_files(data))
	elif args.string:
		receive_input_data()
