import random
class HelperClass:

	def read_file_into_array(file_path):
		with open(file_path, 'r') as file:
			lines = [line.strip() for line in file.readlines()]
		return lines

	def return_random_array_elt(array):
		return array[int(random.random() * 1000 % len(array))]

