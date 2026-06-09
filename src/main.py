from textnode import *
import shutil
from inline_markdown import *
from htmlnode import *
from markdown_blocks import *
from gencontent import *
import os
import sys

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

def generate_recursion(source_folder, destination_folder, basepath):
	for item in os.listdir(source_folder):
		source_path = os.path.join(source_folder, item)
		destination_path = os.path.join(destination_folder, item)

		if os.path.isfile(source_path):
			base, ext = os.path.splitext(destination_path)
			destination_filename = base + ".html"
			generate_page(source_path, "template.html", destination_filename, basepath)
		
		elif os.path.isdir(source_path):
			print(f"checking file{destination_path}")
			generate_recursion(source_path, destination_path, basepath)


def copystatic(dest):
	if os.path.exists("static"):
		if os.path.exists(dest):
			shutil.rmtree(dest)
		os.mkdir(dest)
		copy_folder("static", dest)
	
def main():
	copystatic("docs")
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = "/"
	print("About to generate page")
	generate_page("content/index.md", "template.html", "docs/index.html", basepath)
	generate_recursion("content", "docs", basepath)
	print("Page generated")

main()
