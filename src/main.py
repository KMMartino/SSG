import shutil
import os
from block_functions import markdown_to_html_node
from pathlib import Path

def main():
    if os.path.exists("public"):
        shutil.rmtree("public/")
    filemover("static", "public")

    generate_pages_recurse("content", "template.html", "public")

def filemover(source, target):
    os.mkdir(target)
    for item in os.listdir(source):
        sourcepath = os.path.join(source, item)
        targetpath = os.path.join(target, item)
        if os.path.isfile(sourcepath):
            shutil.copy(sourcepath, targetpath)
        elif os.path.isdir(sourcepath):
            filemover(sourcepath, targetpath)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    
    raise Exception("no title found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    document = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(document)

def generate_pages_recurse(from_path, template_path, dest_path):
    for item in os.listdir(from_path):
        sourcepath = os.path.join(from_path, item)
        targetpath = os.path.join(dest_path, item)
        p_targetpath = Path(targetpath)
        outputpath = p_targetpath.with_suffix(".html")
        if os.path.isfile(sourcepath):
            generate_page(sourcepath, template_path, outputpath)
        elif os.path.isdir(sourcepath):
            generate_pages_recurse(sourcepath, template_path, targetpath)
        

if __name__ == "__main__":
    main()