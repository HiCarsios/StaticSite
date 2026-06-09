from markdown_blocks import *
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            rstring = line[1:]
            result = rstring.strip()
            return result
    raise Exception("No header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        fp_contents = f.read()
    with open(template_path) as t:
        tp_contents = t.read()
    HTML_code = markdown_to_html_node(fp_contents)
    HTML_code = HTML_code.to_html()
    title = extract_title(fp_contents)
    templar = tp_contents.replace("{{ Content }}", HTML_code)
    templar= templar.replace("{{ Title }}", title)
    templar = templar.replace('href="/', f'href="{basepath}')
    templar = templar.replace('src="/', f'href="{basepath}')
    dest_folder = os.path.dirname(dest_path)
    os.makedirs(dest_folder, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(templar)