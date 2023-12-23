import random
import json

class HelperClass:


	def load_json_file(file_path):
		try:
			with open(file_path, 'r') as file:
				json_data = json.load(file)
			return json_data
		except FileNotFoundError:
			print(f"Error: File not found at {file_path}")
			return None
		except json.JSONDecodeError as e:
			print(f"Error decoding JSON file at {file_path}: {e}")
			return None

	def read_file_into_array(file_path):
		with open(file_path, 'r') as file:
			lines = [line.strip() for line in file.readlines()]
		return lines

	def return_random_array_elt(array):
		return array[int(random.random() * 1000 % len(array))]

	def concat_array(array) -> str:
		return ",".join(array)
