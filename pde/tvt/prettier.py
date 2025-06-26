import os
import re


def convert_indentation_to_tabs(file_path, spaces_per_tab=4):
	with open(file_path, "r") as file:
		lines = file.readlines()

	converted_lines = []
	pattern = re.compile(rf"^((?: {{{spaces_per_tab}}})+)")

	for line in lines:
		match = pattern.match(line)
		if match:
			space_groups = len(match.group(1)) // spaces_per_tab
			new_indent = "\t" * space_groups
			rest_of_line = line[len(match.group(1)) :]
			converted_lines.append(new_indent + rest_of_line)
		else:
			converted_lines.append(line)

	with open(file_path, "w") as file:
		file.writelines(converted_lines)


def convert_folder(folder_path, extensions=(".py",)):
	for root, dirs, files in os.walk(folder_path):
		for filename in files:
			if filename.endswith(extensions):
				full_path = os.path.join(root, filename)
				try:
					convert_indentation_to_tabs(full_path)
					print(f"Converted: {full_path}")
				except Exception as e:
					print(f"Failed to convert {full_path}: {e}")


if __name__ == "__main__":
	import sys

	folder = sys.argv[1] if len(sys.argv) > 1 else "."
	convert_folder(folder)
