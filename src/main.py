from textnode import *
import shutil
from inline_markdown import *
from htmlnode import *
from markdown_blocks import *
import os

def inspect_folder(folder):
	paths = []
	for item in os.listdir(folder):
		item_path = os.path.join(folder,item)

		if os.path.isfile(item_path):
			paths.append(item_path)

		if os.path.isdir(item_path):
			paths.extend(inspect_folder(item_path))
	return paths

def copy_folder(source_folder, destination_folder):
	for item in os.listdir(source_folder):
		source_path = os.path.join(source_folder, item)
		destination_path = os.path.join(destination_folder, item)

		if os.path.isfile(source_path):
			shutil.copy(source_path, destination_path)
			print(f"Copying {source_path} to {destination_path}")
		
		elif os.path.isdir(source_path):
			os.mkdir(destination_path)
			print(f"adding file{destination_path}")
			copy_folder(source_path, destination_path)


def copystatic():
	if os.path.exists("static"):
		if os.path.exists("public"):
			shutil.rmtree("public")
		os.mkdir("public")
		copy_folder("static", "public")
	
def main():
	copystatic()


main()
