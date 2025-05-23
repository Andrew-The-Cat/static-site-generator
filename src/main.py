from textnode import *
from htmlnode import *
from doc_parser import *

import os
import shutil
import sys

def reset():
    src_path = "static"
    dest_path = "docs"

    shutil.rmtree(dest_path)
    os.mkdir(dest_path)

    entries = os.listdir(src_path)

    def recursive(entries, src_path, public_path):
        print(f"Copying from {src_path} to {public_path}\n============================================\n")

        for entry in entries:
            src_file = os.path.join(".", src_path, entry)
            public_file = os.path.join(".", public_path, entry)
            if not os.path.exists(src_file):
                return None

            if os.path.isfile(src_file):
                print(f"Copying {os.path.realpath(src_file)}  \n\t---> {os.path.realpath(public_file)}")
                shutil.copy(src_file, public_file)
                continue
 
            # source is not a file, so it must be a directory
            if not os.path.exists(public_file):
                os.mkdir(public_file)

            print(f"Found directory {src_file} ; copying recursively \n\n")
            recursive (os.listdir(src_file), src_file, public_file)

    recursive(entries, src_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    contents = ""
    template = ""

    with open(from_path) as md:
        with open(template_path) as trans:
            contents = md.read()
            template = trans.read()

    html = md_to_html(contents).to_html()
    title = extract_title(contents)

    template = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html).replace(r'href="/', f'href="{basepath}').replace(r'src="/', f'src="{basepath}')

    aux = dest_path.split('/')
    aux.pop()

    path = "."
    for item in aux:
        path = os.path.join(path, item)
        if not os.path.exists(path):
            os.mkdir(path)

    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages(src_dir_path, template_path, dest_dir_path, basepath):
    entries = os.listdir(src_dir_path)

    def recursive(entries, src_path, dest_path):
        for entry in entries:
            src_file = os.path.join(src_path, entry)
            dest_file = os.path.join(dest_path, entry)

            if os.path.isfile(src_file):
                generate_page(src_file, template_path, dest_file.split('.')[0] + '.html', basepath)
                continue

            n_entries = os.listdir(src_file)
            recursive(n_entries, src_file, dest_file)

    recursive(entries, src_dir_path, dest_dir_path)

def main():
    basepath = '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    reset()
    print('')
    generate_pages("content", "template.html", "docs", basepath)
    print('')


main()